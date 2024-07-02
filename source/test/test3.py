def get_neighbors(row, col, max_row, max_col):
    neighbors = []
    for r in range(max(0, row - 1), min(max_row, row + 2)):
        for c in range(max(0, col - 1), min(max_col, col + 2)):
            if (r, c) != (row, col):
                neighbors.append((r, c))
    return neighbors

def generate_minesweeper_rules(max_row, max_col):
    rules = []
    
    # Regole per celle con N_riga_colonna_0
    for row in range(max_row):
        for col in range(max_col):
            # Genera la lista dei vicini
            neighbors = get_neighbors(row, col, max_row, max_col)
            
            # Regola per N_riga_colonna_0
            premise = f"N_{row}_{col}_0"
            for nr, nc in neighbors:
                consequence = f"N_{nr}_{nc}_0"
                rules.append(f"{premise} ==> {consequence}")
    
    # Regole per celle con N_riga_colonna_numero > 0
    for row in range(max_row):
        for col in range(max_col):
            for num in range(1, 9):  # In un campo 4x4, al massimo può avere 8 bombe adiacenti
                # Genera la lista dei vicini
                neighbors = get_neighbors(row, col, max_row, max_col)
                
                # Regola per N_riga_colonna_numero > 0
                premise = f"N_{row}_{col}_{num}"
                for nr, nc in neighbors:
                    bomb_consequence = f"B_{nr}_{nc}"
                    safe_consequence = f"N_{nr}_{nc}_0"
                    rules.append(f"{premise} ==> {bomb_consequence}")
                    rules.append(f"{premise} ==> {safe_consequence}")
    
    return rules

# Eseguiamo la funzione per generare le regole per un campo 4x4
rules = generate_minesweeper_rules(4, 4)

# Stampa delle regole generate
print(len(rules))
for rule in rules[100:200]:
    print(rule)
