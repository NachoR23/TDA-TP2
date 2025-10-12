# === TP2: Algoritmo de Programación Dinámica (Optimizar Ataques) ===
# Ignacio Julián Rodríguez

# Carpeta donde están los archivos de prueba fijos
TEST_DIR = pruebas

# Archivo principal
MAIN = tp2.py

# Archivo de medición de complejidad
BENCH = analisis.py


# ===== COMANDOS =====

# Ejecuta los tests fijos (por defecto)
# Uso: make
run:
	@echo "== Ejecutando casos de prueba fijos =="
	@if [ -d $(TEST_DIR) ]; then \
		for file in $(TEST_DIR)/*.txt; do \
			echo "\n📂 Caso: $$file"; \
			python3 $(MAIN) $$file || exit 1; \
		done; \
	else \
		echo "⚠️  No se encontró la carpeta '$(TEST_DIR)'. Creala y poné los archivos .txt dentro."; \
	fi


# Ejecuta los tests aleatorios y genera gráfico de complejidad
# Uso: make test
test:
	@echo "== Ejecutando mediciones aleatorias y verificando complejidad O(n²) =="
	@python3 $(BENCH)


# Limpia archivos generados
# Uso: make clean
clean:
	@echo "🧹 Limpiando archivos generados..."
	@rm -f verificacion_complejidad_n2.png
	@echo "✔️  Limpieza completa."
