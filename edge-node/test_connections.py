import os
import sys
import time
import psycopg2
import redis

# Configuración obtenida directamente del entorno de red de Docker
DB_HOST = os.getenv("DB_HOST", "nodo_edge_postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "hospital_db")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASS", "admin")

REDIS_HOST = os.getenv("REDIS_HOST", "nodo_edge_redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

def test_postgresql():
    print("⏳ Conectando a PostgreSQL en {}:{}...".format(DB_HOST, DB_PORT))
    try:
        # Intentar la conexión física
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            connect_timeout=5
        )
        cursor = conn.cursor()
        
        # 1. Crear la tabla y asegurar que se guarde el cambio inmediatamente
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prueba_persistente (
                id SERIAL PRIMARY KEY,
                mensaje VARCHAR(100) NOT NULL,
                creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit() # Asegura que la tabla exista físicamente antes del siguiente paso
        
        # 2. Insertar el registro de prueba
        cursor.execute("INSERT INTO prueba_persistente (mensaje) VALUES ('Conexion verificada con exito');")
        conn.commit()
        
        # 3. Consultar cuántos registros hay
        cursor.execute("SELECT COUNT(*) FROM prueba_persistente;")
        cantidad = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        print("✅ [PostgreSQL] Conexión establecida e inserción completada. Total registros: {}".format(cantidad))
        return True
    except Exception as e:
        print("❌ [PostgreSQL] Error de conexión: {}".format(e))
        return False

def test_redis():
    print("⏳ Conectando a Redis en {}:{}...".format(REDIS_HOST, REDIS_PORT))
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, socket_timeout=5)
        
        clave_prueba = "sensor_status:1"
        valor_prueba = "ONLINE_5G"
        
        r.set(clave_prueba, valor_prueba, ex=60)
        valor_recuperado = r.get(clave_prueba).decode('utf-8')
        
        if valor_recuperado == valor_prueba:
            print("✅ [Redis] Escritura y lectura exitosas. Dato recuperado: '{}'".format(valor_recuperado))
            return True
        else:
            print("❌ [Redis] Los datos no coinciden.")
            return False
    except Exception as e:
        print("❌ [Redis] Error de conexión: {}".format(e))
        return False

if __name__ == "__main__":
    print("\n--- INICIANDO PRUEBAS DE INTEGRACIÓN DE BASES DE DATOS ---")
    time.sleep(1)
    
    postgres_ok = test_postgresql()
    redis_ok = test_redis()
    
    if postgres_ok and redis_ok:
        print("\n🎉 [ÉXITO] Todos los sistemas de almacenamiento están interconectados.\n")
        sys.exit(0)
    else:
        print("\n⚠️ [FALLO] Uno o más componentes no pudieron interconectarse.\n")
        sys.exit(1)