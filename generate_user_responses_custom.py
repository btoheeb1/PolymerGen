
import random
import argparse

def generate_ring():
    monomer = random.choice(["A", "B", "C"])
    num_monomers = random.randint(5, 30)
    bond_length = random.choice([1.0, 1.5])
    chain_lengths = random.choices(range(2, 10), k=num_monomers)
    return f"ring {monomer} {num_monomers} {bond_length} " + " ".join(map(str, chain_lengths)) + "\n"

def generate_star():
    num_arms = random.randint(3, 6)
    bond_length = random.choice([1.0, 1.5])
    core_monomer = random.choice(["X", "Y", "Z"])
    monomer_counts = [random.randint(2, 5) for _ in range(num_arms)]
    arm_monomers = random.choices(["A", "B", "C"], k=num_arms)
    components = [str(num_arms), str(bond_length), core_monomer]
    for count, mono in zip(monomer_counts, arm_monomers):
        components += [str(count), mono]
    return "star " + " ".join(components) + "\n"

def generate_block():
    block_count = random.randint(2, 4)
    monomer_types = random.choices(["A", "B", "C", "D"], k=block_count)
    monomer_counts = [random.randint(2, 10) for _ in range(block_count)]
    components = [str(block_count)]
    for mono, count in zip(monomer_types, monomer_counts):
        components += [mono, str(count)]
    return "block " + " ".join(components) + "\n"

def generate_graft():
    main_monomer = random.choice(["A", "B"])
    main_chain_length = random.randint(5, 15)
    num_attachments = random.randint(1, 4)
    components = [main_monomer, str(main_chain_length), str(num_attachments)]
    for _ in range(num_attachments):
        pos = random.randint(1, main_chain_length)
        mono = random.choice(["C", "D", "E"])
        length = random.randint(2, 6)
        components += [str(pos), mono, str(length)]
    return "graft " + " ".join(components) + "\n"

def generate_user_responses(output_file, counts):
    generators = {
        "ring": generate_ring,
        "star": generate_star,
        "block": generate_block,
        "graft": generate_graft,
        "bottlebrush": generate_graft  # alias
    }

    responses = []
    for ptype, count in counts.items():
        if ptype not in generators:
            print(f"Unknown polymer type: {ptype}")
            continue
        for _ in range(count):
            responses.append(generators[ptype]())

    random.shuffle(responses)

    with open(output_file, "w") as f:
        f.writelines(responses)

    print(f"Generated {len(responses)} responses to '{output_file}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate user_responses.txt for specified polymer types.")
    parser.add_argument("--ring", type=int, default=0, help="Number of ring polymers")
    parser.add_argument("--star", type=int, default=0, help="Number of star polymers")
    parser.add_argument("--block", type=int, default=0, help="Number of block polymers")
    parser.add_argument("--graft", type=int, default=0, help="Number of graft polymers")
    parser.add_argument("--bottlebrush", type=int, default=0, help="Number of bottlebrush polymers")
    parser.add_argument("--output", type=str, default="user_responses.txt", help="Output filename")

    args = parser.parse_args()

    counts = {
        "ring": args.ring,
        "star": args.star,
        "block": args.block,
        "graft": args.graft,
        "bottlebrush": args.bottlebrush
    }

    generate_user_responses(args.output, counts)
