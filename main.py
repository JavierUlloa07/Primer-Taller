import csv
import json
from pathlib import Path

IVA = 1.21
CARPETA = Path(__file__).parent

with (CARPETA / "data.json").open("r", encoding="utf-8") as archivo:
    data = json.load(archivo)

# 1. Gasto total por usuario
print("1. GASTO TOTAL POR USUARIO")
gastos = {
    usuario: round(sum(compra["precio"] for compra in compras), 2)
    for usuario, compras in data.items()
}
for usuario, total in gastos.items():
    print(f"   {usuario}: {total:.2f} €")

# 2. Cliente VIP
if gastos:
    vip = max(gastos, key=gastos.get)
    print(f"\n2. CLIENTE VIP: {vip} con {gastos[vip]:.2f} €")

# 3. Cliente con más artículos
articulos = {usuario: len(compras) for usuario, compras in data.items()}
if articulos:
    mas_articulos = max(articulos, key=articulos.get)
    print(f"\n3. MÁS ARTÍCULOS: {mas_articulos} con {articulos[mas_articulos]} productos")

# Lista de compras junto al nombre de usuario
compras_totales = [
    (usuario, compra)
    for usuario, compras in data.items()
    for compra in compras
]

# 4. Producto más caro y más barato
print("\n4. PRODUCTO MÁS CARO Y MÁS BARATO")
if compras_totales:
    usuario_caro, producto_caro = max(compras_totales, key=lambda fila: fila[1]["precio"])
    usuario_barato, producto_barato = min(compras_totales, key=lambda fila: fila[1]["precio"])
    print(f"   Más caro: {producto_caro['producto']} - {producto_caro['precio']:.2f} € (comprado por {usuario_caro})")
    print(f"   Más barato: {producto_barato['producto']} - {producto_barato['precio']:.2f} € (comprado por {usuario_barato})")
else:
    print("   No hay compras registradas.")

# 5. Gasto por categorías
categorias = {}
for _, compra in compras_totales:
    categoria = compra["categoria"]
    categorias[categoria] = categorias.get(categoria, 0) + compra["precio"]
categorias = {categoria: round(total, 2) for categoria, total in categorias.items()}
print("\n5. RESUMEN POR CATEGORÍAS")
print(f"   {categorias}")

# 6. Añadir precio con IVA
for _, compra in compras_totales:
    compra["precioIVA"] = round(compra["precio"] * IVA, 2)
print("\n6. PRODUCTOS CON IVA")
for usuario, compra in compras_totales:
    print(f"   {usuario}: {compra['producto']} -> {compra['precio']:.2f} € / {compra['precioIVA']:.2f} € con IVA")

# 7. Crear el CSV en la misma carpeta que este programa
ruta_csv = CARPETA / "contabilidad_a.csv"
with ruta_csv.open("w", newline="", encoding="utf-8-sig") as archivo:
    escritor = csv.writer(archivo)
    escritor.writerow(["producto", "precioIVA"])
    for _, compra in compras_totales:
        escritor.writerow([compra["producto"], f"{compra['precioIVA']:.2f}"])
print(f"\n7. Fichero '{ruta_csv.name}' creado.")
