#!/usr/bin/env python3
"""
Sistema de Prefill Solo Excel - Sin envío de emails
Motor de prefill que genera únicamente tabla Excel con links para envío manual
"""

from prefill_engine_v2 import PrefillEngineV2
from datetime import datetime

def main():
    """Ejecutar solo generación de Excel"""
    print("=" * 70)
    print("📊 PREFILL ENGINE - MODO SOLO EXCEL")
    print("=" * 70)
    print("✅ Sin envío automático de emails")
    print("📊 Generando tabla Excel con links de prefill")
    print("📝 Creando templates de email para copiar y pegar")
    print("=" * 70)
    
    engine = PrefillEngineV2()
    
    try:
        # Ejecutar flujo completo sin emails
        success = engine.run_complete_workflow(
            send_emails=False,      # No enviar emails
            generate_excel=True     # Sí generar Excel
        )
        
        if success:
            print(f"\n🎉 ¡TABLA EXCEL GENERADA EXITOSAMENTE!")
            print(f"\n📋 PRÓXIMOS PASOS:")
            print(f"   1. Abrir archivo Excel en ../outputs/")
            print(f"   2. Copiar links de columna 'Link de Prefill'")
            print(f"   3. Enviar manualmente por email corporativo")
            print(f"   4. Usar templates generados como referencia")
            
        else:
            print(f"\n❌ Problemas en la generación de Excel")
            
    except KeyboardInterrupt:
        print("\n\n⏸️  Procesamiento cancelado por usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()