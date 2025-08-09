"""
Setup Validator - Validates JotForm API configuration and connectivity
Optimized setup script for the 5REC JotForm integration system
"""

import requests
import sys
import json
from datetime import datetime
from config import JOTFORM_API_KEY, FORM_ID

class JotFormSetupValidator:
    """Validates JotForm API setup and configuration"""
    
    def __init__(self):
        self.api_key = JOTFORM_API_KEY
        self.form_id = FORM_ID
        self.base_url = "https://api.jotform.com"
        self.headers = {"APIKEY": self.api_key}
        self.results = {}
    
    def validate_config(self):
        """Validate configuration variables"""
        print("🔍 Validando configuración...")
        
        if not self.api_key:
            print("❌ Error: JOTFORM_API_KEY no está configurado")
            return False
            
        if not self.form_id:
            print("❌ Error: FORM_ID no está configurado")
            return False
            
        print("✅ Variables de configuración válidas")
        return True
    
    def test_api_connection(self):
        """Test basic API connectivity"""
        print("\n🌐 Probando conexión API...")
        
        try:
            url = f"{self.base_url}/user"
            response = requests.get(url, headers=self.headers, timeout=10)
            data = response.json()
            
            if response.status_code == 200 and data.get('responseCode') == 200:
                user_info = data.get('content', {})
                print(f"✅ API conectada exitosamente")
                print(f"   Usuario: {user_info.get('name', 'N/A')}")
                print(f"   Email: {user_info.get('email', 'N/A')}")
                self.results['api_connection'] = True
                return True
            else:
                print(f"❌ Error API: {data.get('message', 'Error desconocido')}")
                self.results['api_connection'] = False
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {e}")
            self.results['api_connection'] = False
            return False
    
    def validate_form_access(self):
        """Validate access to specific form"""
        print(f"\n📋 Validando acceso al formulario {self.form_id}...")
        
        try:
            url = f"{self.base_url}/form/{self.form_id}"
            response = requests.get(url, headers=self.headers, timeout=10)
            data = response.json()
            
            if response.status_code == 200 and data.get('responseCode') == 200:
                form_info = data.get('content', {})
                print(f"✅ Formulario accesible")
                print(f"   Título: {form_info.get('title', 'N/A')}")
                print(f"   Estado: {form_info.get('status', 'N/A')}")
                print(f"   Creado: {form_info.get('created_at', 'N/A')}")
                self.results['form_access'] = True
                return True
            else:
                print(f"❌ Error acceso formulario: {data.get('message', 'Error desconocido')}")
                self.results['form_access'] = False
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error validando formulario: {e}")
            self.results['form_access'] = False
            return False
    
    def get_form_statistics(self):
        """Get basic form statistics"""
        print(f"\n📊 Obteniendo estadísticas del formulario...")
        
        try:
            # Get form questions
            url = f"{self.base_url}/form/{self.form_id}/questions"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('responseCode') == 200:
                    questions = data.get('content', {})
                    print(f"✅ Total de campos: {len(questions)}")
                    
                    # Count field types
                    field_types = {}
                    for q in questions.values():
                        field_type = q.get('type', 'unknown')
                        field_types[field_type] = field_types.get(field_type, 0) + 1
                    
                    print("   Tipos de campos:")
                    for field_type, count in sorted(field_types.items()):
                        print(f"   - {field_type}: {count}")
                    
                    self.results['form_statistics'] = {
                        'total_fields': len(questions),
                        'field_types': field_types
                    }
                    return True
            
            print("⚠️  No se pudieron obtener estadísticas")
            return False
            
        except Exception as e:
            print(f"❌ Error obteniendo estadísticas: {e}")
            return False
    
    def run_full_validation(self):
        """Run complete setup validation"""
        print("=" * 60)
        print("🚀 VALIDADOR DE SETUP - SISTEMA 5REC JOTFORM")
        print("=" * 60)
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all validations
        config_ok = self.validate_config()
        if not config_ok:
            print("\n❌ Validación fallida - Revisar configuración")
            return False
        
        api_ok = self.test_api_connection()
        if not api_ok:
            print("\n❌ Validación fallida - Problemas de conexión API")
            return False
        
        form_ok = self.validate_form_access()
        if not form_ok:
            print("\n❌ Validación fallida - Sin acceso al formulario")
            return False
        
        self.get_form_statistics()
        
        print("\n" + "=" * 60)
        print("✅ SETUP VALIDADO EXITOSAMENTE")
        print("✅ Sistema listo para usar")
        print("=" * 60)
        
        return True
    
    def save_validation_report(self):
        """Save validation results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"../outputs/SETUP_VALIDATION_{timestamp}.json"
        
        report = {
            'timestamp': timestamp,
            'validation_results': self.results,
            'configuration': {
                'form_id': self.form_id,
                'api_key_configured': bool(self.api_key)
            }
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"\n📄 Reporte guardado: {filename}")
        except Exception as e:
            print(f"\n⚠️  No se pudo guardar reporte: {e}")

def main():
    """Main execution function"""
    validator = JotFormSetupValidator()
    
    try:
        success = validator.run_full_validation()
        validator.save_validation_report()
        
        if success:
            print(f"\n➡️  Próximo paso: Ejecutar formMetadata.py para análisis detallado")
        else:
            print(f"\n🔧 Revisar configuración en .env antes de continuar")
            
    except KeyboardInterrupt:
        print("\n\n⏸️  Validación cancelada por usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
    
    input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()