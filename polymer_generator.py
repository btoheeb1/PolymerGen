
import os
import numpy as np
import pandas as pd
import math

def ensure_directory_exists(folder):
    os.makedirs(folder, exist_ok=True)

def ring_polymer(monomer, num_monomers, bond_length, chain_lengths):
    angle = 2 * math.pi / num_monomers
    coordinates = []
    pdb_lines = []
    connect_lines = []

    for i in range(num_monomers):
        x = ((num_monomers - 1) * bond_length / 5.71) * math.cos(i * angle)
        y = 0.0
        z = ((num_monomers - 1) * bond_length / 5.71) * math.sin(i * angle)
        coordinates.append((x, y, z))

        serial_number = i + 1
        atom_name = monomer
        residue_name = monomer
        chain_id = monomer
        residue_number = i + 1
        occupancy = 1.0
        temperature_factor = 0.0
        element_symbol = monomer

        pdb_line = f"ATOM  {serial_number:5}  {atom_name:3} {residue_name:<2} {chain_id:1}{residue_number:>5}    {x:8.3f}{y:8.3f}{z:8.3f}{occupancy:6.2f}{temperature_factor:6.2f}          {element_symbol:2}\n"
        pdb_lines.append(pdb_line)

        serial_number1 = i + 1
        serial_number2 = i + 2 if i < num_monomers - 1 else 1
        connect_line = f"CONECT {serial_number1:4} {serial_number2:4}\n"
        connect_lines.append(connect_line)

    monomer_index = num_monomers + 1
    used_serial_numbers = set()

    for i in range(num_monomers):
        chain_length = chain_lengths[i]
        chain_start = monomer_index
        chain_end = chain_start + chain_length - 1

        for j in range(chain_start, chain_end + 1):
            x_chain = coordinates[i][0]
            y_chain = j - chain_start + 1
            z_chain = coordinates[i][2]
            coordinates.append((x_chain, y_chain, z_chain))

            while monomer_index in used_serial_numbers:
                monomer_index += 1

            used_serial_numbers.add(monomer_index)
            serial_number_chain = monomer_index
            residue_number_chain = j

            pdb_line_chain = f"ATOM  {serial_number_chain:5}  {atom_name:3} {residue_name:<2} {chain_id:1}{residue_number_chain:>5}    {x_chain:8.3f}{y_chain:8.3f}{z_chain:8.3f}{occupancy:6.2f}{temperature_factor:6.2f}          {element_symbol:2}\n"
            pdb_lines.append(pdb_line_chain)

            if j > chain_start:
                connect_line_chain = f"CONECT {serial_number_chain - 1:4} {serial_number_chain:4}\n"
                connect_lines.append(connect_line_chain)

            monomer_index += 1

        connect_line_chain_start = f"CONECT {chain_start:4} {i + 1:4}\n"
        connect_lines.append(connect_line_chain_start)

    pdb_lines.append("END\n")
    pdb_content = ''.join(pdb_lines + connect_lines)

    output_dir = "outputs/ring"
    ensure_directory_exists(output_dir)
    output_filename = f"{output_dir}/ring_polymer_{num_monomers}_{chain_lengths}_{bond_length}.pdb"
    with open(output_filename, 'w') as output_file:
        output_file.write(pdb_content)

def star_polymer(num_arms, bond_length, core_monomer, monomer_counts, arm_monomers):
    core_coords = np.array([[0.0, 0.0, 0.0]])
    arm_coords = np.zeros((sum(monomer_counts), 3))
    idx = 0
    for i in range(num_arms):
        theta = 2 * np.pi * i / num_arms
        for j in range(monomer_counts[i]):
            r = (j + 1) * bond_length
            arm_coords[idx] = [r * np.cos(theta), r * np.sin(theta), 0.0]
            idx += 1

    df = pd.DataFrame(core_coords, columns=['x', 'y', 'z'], index=[1])
    df = pd.concat([df, pd.DataFrame(arm_coords, columns=['x', 'y', 'z'], index=range(2, sum(monomer_counts) + 2))])

    occupancy = 1.0
    temperature_factor = 0.0

    output_dir = "outputs/star"
    ensure_directory_exists(output_dir)
    output_filename = f"{output_dir}/star_polymer_{num_arms}_{bond_length}_{core_monomer}.pdb"

    with open(output_filename, 'w') as pdb_file:
        pdb_file.write("HEADER    Star-Shaped Polymer\n")
        for idx, row in df.iterrows():
            if idx == 1:
                monomer_type = core_monomer
            else:
                arm_idx = next(i for i, count in enumerate(monomer_counts) if idx <= 1 + sum(monomer_counts[:i+1]))
                monomer_type = arm_monomers[arm_idx]

            atom_name = monomer_type
            residue_name = monomer_type
            element_symbol = monomer_type
            pdb_file.write(f"ATOM  {idx:5d}  {atom_name:<4s} {residue_name:<3s}{idx:4d}    {row['x']:8.3f}{row['y']:8.3f}{row['z']:8.3f}{occupancy:6.2f}{temperature_factor:6.2f}           {element_symbol:2}\n")

        for i in range(num_arms):
            first_monomer_idx = sum(monomer_counts[:i]) + 2
            pdb_file.write(f"CONECT    1 {first_monomer_idx:4d}\n")
            for j in range(monomer_counts[i] - 1):
                current_monomer_idx = sum(monomer_counts[:i]) + j + 2
                next_monomer_idx = sum(monomer_counts[:i]) + j + 3
                pdb_file.write(f"CONECT {current_monomer_idx:4d} {next_monomer_idx:4d}\n")

        pdb_file.write("END\n")

def linear_with_blocks(monomer_counts):
    pdb_file = ""
    block_count = len(monomer_counts)
    chain_length = sum(monomer_counts)

    for i in range(chain_length):
        atom_serial = i + 1
        residue_serial = i + 1
        atom_name = "ATOM"
        occupancy = 1
        temperature_factor = 0.0
        x, y, z = i * 1, i * 1, i * 1

        block_index = 0
        monomer = chr(65 + block_index)
        monomer_count_sum = 0

        for count in monomer_counts:
            if residue_serial <= monomer_count_sum + count:
                monomer = chr(65 + block_index)
                break
            monomer_count_sum += count
            block_index += 1

        element_symbol = monomer
        atom_line = f"ATOM  {atom_serial:5}  {monomer:3} {monomer:<3} {residue_serial:>5}    {x:8.3f}{y:8.3f}{z:8.3f}{occupancy:6.2f}{temperature_factor:6.2f}          {element_symbol:2}\n"
        pdb_file += atom_line

    for i in range(1, chain_length):
        bonding_line = f"CONECT {i:4}{i + 1:4}\n"
        pdb_file += bonding_line

    output_dir = "outputs/block"
    ensure_directory_exists(output_dir)
    file_name = f"{output_dir}/block_polymer_{block_count}_{len(monomer_counts)}_{'+'.join(map(str, monomer_counts))}.pdb"
    with open(file_name, "w") as f:
        f.write(pdb_file)


def graft_polymer(main_monomer, main_chain_length, attachment_positions, polymer_type="graft"):
    pdb_file = ""

    atom_serial = 1
    residue_serial = 1

    atom_lines = []
    bonding_lines = []

    for i in range(1, main_chain_length + 1):
        atom_name = "ATOM"
        residue_name = main_monomer
        x, y, z = (i - 1) * 1.0, 0.0, 0.0

        occupancy = 1.0
        temperature_factor = 0.0
        element_symbol = main_monomer

        atom_line = f"{atom_name:6}{atom_serial:5} {main_monomer:^3} {main_monomer:4}{residue_serial:6}    {x:8.3f}{y:8.3f}{z:8.3f}{occupancy:6.2f}{temperature_factor:6.2f}          {element_symbol:2}\n"
        atom_lines.append(atom_line)

        atom_serial += 1
        residue_serial += 1

    attachment_serial = main_chain_length + 1
    for attachment_pos, (additional_monomer, additional_chain_length) in attachment_positions:
        additional_atom_lines = []

        start_x, start_y, start_z = (attachment_pos - 1) * 1.0, 1.0, 0.0

        for i in range(additional_chain_length):
            atom_name = "ATOM"
            residue_name = additional_monomer
            x = start_x
            y = start_y + i * 1.0
            z = start_z

            occupancy = 1.0
            temperature_factor = 0.0
            element_symbol = additional_monomer

            atom_line = f"{atom_name:6}{atom_serial:5} {additional_monomer:^3} {residue_name:4}{attachment_serial:6}    {x:8.3f}{y:8.3f}{z:8.3f}{occupancy:6.2f}{temperature_factor:6.2f}          {element_symbol:2}\n"
            additional_atom_lines.append(atom_line)

            atom_serial += 1
            attachment_serial += 1

        bonding_line = f"CONECT {attachment_pos:4}{attachment_serial - additional_chain_length:4}\n"
        bonding_lines.append(bonding_line)

        for i in range(len(additional_atom_lines) - 1):
            bonding_line = f"CONECT {attachment_serial - additional_chain_length + i:4}{attachment_serial - additional_chain_length + i + 1:4}\n"
            bonding_lines.append(bonding_line)

        atom_lines.extend(additional_atom_lines)

    for i in range(1, main_chain_length):
        bonding_line = f"CONECT {i:4}{i + 1:4}\n"
        bonding_lines.append(bonding_line)

    pdb_file += "".join(atom_lines)
    pdb_file += "".join(bonding_lines)

    residue_serial = main_chain_length + sum([length for _, (_, length) in attachment_positions])
    residue_line = f"TER   {residue_serial:5}      {main_monomer:4}\n"
    pdb_file += residue_line

    output_dir = f"outputs/{polymer_type}"
    ensure_directory_exists(output_dir)
    filename = f"{output_dir}/{polymer_type}_polymer_{len(attachment_positions)}_{attachment_positions}.pdb"
    with open(filename, "w") as pdb_file_obj:
        pdb_file_obj.write(pdb_file)

#    print(f"Graft polymer '{main_monomer}' generated and saved as '{filename}'.")

# Driver loop
with open("user_responses.txt", "r") as file:
    lines = file.readlines()

for line in lines:
    line = line.strip()
    if line:
        polymer_type, *user_responses = line.split()

        if polymer_type == "ring":
            monomer = user_responses[0]
            num_monomers = int(user_responses[1])
            bond_length = float(user_responses[2])
            chain_lengths = list(map(int, user_responses[3:]))
            ring_polymer(monomer, num_monomers, bond_length, chain_lengths)

        elif polymer_type == "star":
            num_arms = int(user_responses[0])
            bond_length = float(user_responses[1])
            core_monomer = user_responses[2]
            monomer_counts = [int(user_responses[i]) for i in range(3, len(user_responses), 2)]
            arm_monomers = user_responses[4::2]
            star_polymer(num_arms, bond_length, core_monomer, monomer_counts, arm_monomers)

        elif polymer_type == "block":
            block_count = int(user_responses[0])
            monomer_counts = []
            for i in range(1, len(user_responses), 2):
                monomer_type = user_responses[i]
                monomer_count = int(user_responses[i + 1])
                monomer_counts.append(monomer_count)

            linear_with_blocks(monomer_counts)

        elif polymer_type in ["graft", "bottlebrush"]:
            main_monomer = user_responses[0]
            main_chain_length = int(user_responses[1])
            num_attachments = int(user_responses[2])
            attachment_positions = []
            for i in range(num_attachments):
                pos = int(user_responses[3 + i * 3])
                monomer = user_responses[4 + i * 3]
                length = int(user_responses[5 + i * 3])
                attachment_positions.append((pos, (monomer, length)))
            graft_polymer(main_monomer, main_chain_length, attachment_positions, polymer_type)

        else:
            print(f"Invalid polymer type '{polymer_type}'. Skipping.")
