
# Polymer Structure Generator

This repository provides a complete system for generating polymer structure files (`.pdb`) for various polymer architectures (star, block, ring, bottle brush with different graft densities) using a combination of:

- **Randomized input generation** (`generate_user_responses_custom.py`)
- **Polymer structure builder** (`polymer_generator.py`)
- **Graphical interfaces**: both CLI and optional Streamlit GUI (`app.py`)

---

##  Repository Structure

```
.
├── app.py                         # Streamlit GUI interface (optional)
├── generate_user_responses_custom.py   # CLI script to generate user_responses.txt
├── polymer_generator.py       # Main structure builder
├── user_responses.txt            # Input file (auto-generated)
├── outputs/                      # Directory where polymer .pdb files are saved
│   ├── ring/
│   ├── star/
│   ├── block/
│   └── graft/
└── README.md                     # You're here
```

---

##  Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/polymer-generator.git
cd PolymerGen
```

### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or if you’re only using the CLI:

```bash
pip install streamlit
```

---

## 🚀 How to Use

### Option 1: Command-Line

Generate the user input file:
```bash
python generate_user_responses_custom.py --ring 5 --star 3 --block 4 --graft 2 --output user_responses.txt
```

Then generate the polymer structures:
```bash
python polymer_generator.py
```

### Option 2: Streamlit GUI (Recommended)

Launch the Streamlit app:
```bash
streamlit run app.py
```

Then open your browser to [http://localhost:8501](http://localhost:8501) and fill out the form to generate and build polymers.

---

##  Output

Polymer `.pdb` files will be saved in the `outputs/` directory in appropriate subfolders like `outputs/ring/`, `outputs/block/`, etc.

---

##  Input Format Reference

Each line in `user_responses.txt` follows a specific format depending on the polymer type:

---

###  Ring Polymer
```
ring <monomer> <num_monomers> <bond_length> <chain1_len> <chain2_len> ... <chainN_len>
```

**Example:**
```
ring A 6 1.0 2 2 2 2 2 2
```
→ A ring of 6 monomers (A), bond length 1.0, each with a 2-unit side chain.

---

###  Block Copolymer
```
block <block_count> <monomer1> <count1> <monomer2> <count2> ...
```

**Example:**
```
block 3 A 4 B 6 C 3
```
→ A 13-unit linear polymer: 4 A’s, 6 B’s, 3 C’s in sequence.

---

###  Star Polymer
```
star <num_arms> <bond_length> <core_monomer> <count1> <mono1> <count2> <mono2> ...
```

**Example:**
```
star 3 1.0 X 2 A 3 B 2 C
```
→ A 3-arm star with core `X` and different monomers on each arm.

---

###  Graft / Bottlebrush Polymer
```
graft <main_monomer> <main_chain_length> <num_attachments> <pos1> <monomer1> <len1> ...
```

**Example:**
```
graft A 6 2 2 B 3 5 C 2
```
→ A 6-unit linear chain of A with:
- a 3-unit B chain at position 2
- a 2-unit C chain at position 5

---

## 👨‍🔬 Author

Toheeb Olamide Balogun 
