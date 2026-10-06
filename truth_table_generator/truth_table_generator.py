import itertools
import re

def tokenize_and_parse(expression_str):
    """
    1. Preprocessing dan Normalisasi Operator Logika
    2. Deteksi Seluruh Variabel Proposisional Unik secara Otomatis
    """
    # Mengonversi operator ke huruf kapital agar standar
    expr = re.sub(r'\band\b', 'AND', expression_str, flags=re.IGNORECASE)
    expr = re.sub(r'\bor\b', 'OR', expr, flags=re.IGNORECASE)
    expr = re.sub(r'\bnot\b', 'NOT', expr, flags=re.IGNORECASE)
    
    # Ekstrak kata/karakter yang merupakan nama variabel (bukan keyword operator)
    tokens = re.findall(r'\b[a-zA-Z_]\w*\b', expr)
    keywords = {'AND', 'OR', 'NOT', 'TRUE', 'FALSE'}
    
    # Ambil variabel unik dan urutkan secara alfabetis
    variables = sorted(list(set(token for token in tokens if token not in keywords)))
    return expr, variables

def python_eval_expr(expr, var_dict):
    """
    Mengubah operator logika ke sintaks Python (and, or, not) 
    lalu mengevaluasi nilai kebenarannya berdasarkan kombinasi variabel.
    """
    # Ganti operator ke sintaks asli Python
    py_expr = expr.replace('AND', ' and ').replace('OR', ' or ').replace('NOT', ' not ')
    
    # Evaluasi ekspresi logika
    return bool(eval(py_expr, {}, var_dict))

def generate_truth_table(expression_str):
    """
    Membangkitkan seluruh 2^n kombinasi nilai kebenaran (T/F),
    mengevaluasi ekspresi, dan mencetak tabel kebenaran yang rapi.
    """
    formatted_expr, variables = tokenize_and_parse(expression_str)
    n = len(variables)
    
    print("=" * 60)
    print(f"Ekspresi Input : {expression_str}")
    print(f"Variabel Unik  : {', '.join(variables)} (n = {n})")
    print(f"Jumlah Baris   : 2^{n} = {2**n} Kombinasi")
    print("=" * 60)
    
    # Header Tabel
    headers = variables + [formatted_expr]
    col_widths = [max(len(var), 3) for var in variables] + [max(len(formatted_expr), 10)]
    
    # Cetak Header
    header_str = " | ".join(f"{h:^{w}}" for h, w in zip(headers, col_widths))
    print(header_str)
    print("-" * len(header_str))
    
    # Pembangkitan 2^n Kombinasi True / False
    combinations = list(itertools.product([True, False], repeat=n))
    
    # Evaluasi & Tampilkan Setiap Baris
    for combo in combinations:
        var_dict = dict(zip(variables, combo))
        result = python_eval_expr(formatted_expr, var_dict)
        
        # Formatting True/False menjadi 'T' atau 'F'
        row_vals = ["T" if v else "F" for v in combo]
        res_val = "T" if result else "F"
        
        # Cetak Baris
        row_str = " | ".join(f"{v:^{w}}" for v, w in zip(row_vals, col_widths[:-1]))
        row_str += f" | {res_val:^{col_widths[-1]}}"
        print(row_str)
    
    print("=" * 60 + "\n")

# ==========================================
# DEMO UTAMA (2 EKSPRESI SESUAI MILESTONE)
# ==========================================
if __name__ == "__main__":
    # Pengujian 1
    generate_truth_table("p AND (q OR NOT r)")

    # Pengujian 2
    generate_truth_table("(p AND q) OR (NOT p AND r)")