"""
Prefill Engine v2.0 - Motor de prefill optimizado sin errores
Sistema completo de prefill con mapeo limpio, validación y emails
"""

import pandas as pd
import requests
import smtplib
import json
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from config import JOTFORM_API_KEY, FORM_ID, GMAIL_USER, GMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT, FROM_NAME

class PrefillEngineV2:
    """Motor de prefill optimizado usando mapeo limpio y API validada"""
    
    def __init__(self):
        self.api_key = JOTFORM_API_KEY
        self.form_id = FORM_ID
        self.base_url = "https://api.jotform.com"
        
        # Email configuration
        self.email_config = {
            'smtp_server': SMTP_SERVER,
            'smtp_port': SMTP_PORT,
            'email_user': GMAIL_USER,
            'email_password': GMAIL_PASSWORD,
            'from_name': FROM_NAME
        }
        
        # Processing data
        self.clean_mapping = {}
        self.excel_data = pd.DataFrame()
        self.results = []
        
    def load_clean_mapping(self):
        """Load validated clean mapping"""
        print("🗺️  Cargando mapeo limpio validado...")
        
        try:
            # Find latest clean mapping
            outputs_dir = Path("../outputs")
            mapping_files = list(outputs_dir.glob("SIMPLE_MAPPING_*.json"))
            
            if mapping_files:
                latest_mapping = max(mapping_files, key=lambda x: x.stat().st_mtime)
                
                with open(latest_mapping, 'r', encoding='utf-8') as f:
                    self.clean_mapping = json.load(f)
                
                print(f"✅ Mapeo cargado: {len(self.clean_mapping)} campos")
                print(f"   Archivo: {latest_mapping.name}")
                return True
            else:
                print("❌ No se encontró archivo de mapeo limpio")
                return False
                
        except Exception as e:
            print(f"❌ Error cargando mapeo: {e}")
            return False
    
    def load_excel_data(self, excel_path="../inputs/TEST.xlsx"):
        """Load and validate Excel data"""
        print(f"📊 Cargando datos desde {excel_path}...")
        
        try:
            # Try main data sheet
            df = pd.read_excel(excel_path, sheet_name="📊 DATOS PREFILL")
            
            # Filter out metadata rows
            filtered_rows = []
            for idx, row in df.iterrows():
                first_value = str(row.iloc[0]) if len(row) > 0 else ""
                # Skip rows that look like metadata
                if not any(keyword in first_value.upper() for keyword in ['TIPO:', 'ID:', 'DESCRIPCIÓN']):
                    filtered_rows.append(row)
            
            if filtered_rows:
                self.excel_data = pd.DataFrame(filtered_rows).reset_index(drop=True)
                print(f"✅ Datos cargados: {len(self.excel_data)} filas, {len(self.excel_data.columns)} columnas")
                
                # Show sample data
                for idx, row in self.excel_data.head(3).iterrows():
                    empresa = row.get('Nombre Empresa/Organización', 'N/A')
                    email = row.get('Email Destinatario', 'N/A')
                    print(f"   Fila {idx}: {empresa} - {email}")
                
                return True
            else:
                print("❌ No se encontraron filas de datos válidas")
                return False
                
        except Exception as e:
            print(f"❌ Error cargando Excel: {e}")
            return False
    
    def create_prefill_submission(self, data_row):
        """Create prefilled submission using validated API method"""
        # Prepare form data using clean mapping
        form_data = {}
        mapped_fields = 0
        
        for excel_column, field_id in self.clean_mapping.items():
            if excel_column in data_row:
                value = data_row[excel_column]
                
                # Clean and validate value
                if pd.isna(value) or str(value).strip() == '':
                    continue  # Skip empty values
                
                # Format value properly
                clean_value = str(value).strip()
                form_data[f"submission[{field_id}]"] = clean_value
                mapped_fields += 1
        
        # API call
        url = f"{self.base_url}/form/{self.form_id}/submissions?apiKey={self.api_key}"
        
        try:
            response = requests.post(url, data=form_data, timeout=30)
            data = response.json()
            
            if response.status_code == 200 and data.get('responseCode') == 200:
                submission_id = data['content']['submissionID']
                edit_url = f"https://www.jotform.com/edit/{submission_id}"
                
                return {
                    'success': True,
                    'submission_id': submission_id,
                    'edit_url': edit_url,
                    'mapped_fields': mapped_fields,
                    'error': None
                }
            else:
                return {
                    'success': False,
                    'submission_id': None,
                    'edit_url': None,
                    'mapped_fields': mapped_fields,
                    'error': data.get('message', f'HTTP {response.status_code}')
                }
                
        except Exception as e:
            return {
                'success': False,
                'submission_id': None,
                'edit_url': None,
                'mapped_fields': mapped_fields,
                'error': str(e)
            }
    
    def send_email(self, to_email, empresa, edit_url, mapped_fields):
        """Send email with prefilled form URL"""
        
        # Create email content
        subject = f"Formulario 5REC Pre-llenado - {empresa}"
        
        html_body = f"""
        <html>
        <head></head>
        <body>
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                    <h2 style="color: #2c5aa0; margin: 0;">🏢 Formulario 5REC</h2>
                    <p style="color: #666; margin: 5px 0 0 0;">Reporte Empresarial Consolidado</p>
                </div>
                
                <div style="background-color: white; padding: 30px; border-radius: 10px; border: 1px solid #e9ecef;">
                    <h3 style="color: #333;">Estimado equipo de <strong>{empresa}</strong>,</h3>
                    
                    <p style="color: #666; line-height: 1.6;">
                        Hemos preparado su formulario 5REC con <strong>{mapped_fields} campos pre-llenados</strong> 
                        basados en la información que nos proporcionaron.
                    </p>
                    
                    <div style="background-color: #e7f3ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <p style="margin: 0; color: #0066cc;">
                            <strong>🔗 Acceder al formulario:</strong>
                        </p>
                        <a href="{edit_url}" 
                           style="display: inline-block; background-color: #2c5aa0; color: white; 
                                  padding: 12px 25px; text-decoration: none; border-radius: 5px; 
                                  margin-top: 10px; font-weight: bold;">
                            ▶️ Abrir Formulario Pre-llenado
                        </a>
                    </div>
                    
                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0;">
                        <p style="margin: 0; color: #666; font-size: 14px;">
                            <strong>📝 Instrucciones:</strong><br>
                            • El formulario ya tiene información básica de su organización<br>
                            • Complete los campos faltantes según corresponda<br>
                            • Guarde y envíe cuando esté completo<br>
                            • El enlace es único y personal para su organización
                        </p>
                    </div>
                    
                    <hr style="border: none; border-top: 1px solid #e9ecef; margin: 30px 0;">
                    
                    <p style="color: #666; font-size: 13px; text-align: center;">
                        <strong>Equipo 5REC</strong><br>
                        Este enlace es válido y puede ser usado para completar su reporte.<br>
                        Si tiene preguntas, no dude en contactarnos.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = f"{FROM_NAME} <{self.email_config['email_user']}>"
            message["To"] = to_email
            
            # Add HTML content
            html_part = MIMEText(html_body, "html")
            message.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.starttls()
                server.login(self.email_config['email_user'], self.email_config['email_password'])
                server.send_message(message)
            
            return {'success': True, 'error': None}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def process_all_organizations(self):
        """Process all organizations in Excel data"""
        print(f"\n🚀 Procesando {len(self.excel_data)} organizaciones...")
        
        for idx, row in self.excel_data.iterrows():
            print(f"\n📋 Procesando organización {idx + 1}/{len(self.excel_data)}")
            
            # Get organization details
            empresa = row.get('Nombre Empresa/Organización', f'Organización_{idx}')
            email_destinatario = row.get('Email Destinatario', '')
            
            print(f"   🏢 Empresa: {empresa}")
            print(f"   📧 Email: {email_destinatario}")
            
            # Skip if no email
            if pd.isna(email_destinatario) or not email_destinatario.strip():
                print(f"   ⚠️  Sin email - omitiendo")
                self.results.append({
                    'empresa': empresa,
                    'email': email_destinatario,
                    'prefill_success': False,
                    'email_success': False,
                    'error': 'No email provided'
                })
                continue
            
            # Create prefilled submission
            print(f"   🔧 Creando submission prefilled...")
            prefill_result = self.create_prefill_submission(row)
            
            result_entry = {
                'empresa': empresa,
                'email': email_destinatario,
                'prefill_success': prefill_result['success'],
                'submission_id': prefill_result.get('submission_id'),
                'edit_url': prefill_result.get('edit_url'),
                'mapped_fields': prefill_result.get('mapped_fields', 0),
                'email_success': False,
                'prefill_error': prefill_result.get('error'),
                'email_error': None
            }
            
            if prefill_result['success']:
                print(f"   ✅ Prefill exitoso - {prefill_result['mapped_fields']} campos")
                print(f"   🔗 URL: {prefill_result['edit_url']}")
                
                # Send email
                print(f"   📧 Enviando email...")
                email_result = self.send_email(
                    email_destinatario, 
                    empresa, 
                    prefill_result['edit_url'],
                    prefill_result['mapped_fields']
                )
                
                result_entry['email_success'] = email_result['success']
                result_entry['email_error'] = email_result.get('error')
                
                if email_result['success']:
                    print(f"   ✅ Email enviado exitosamente")
                else:
                    print(f"   ❌ Error email: {email_result['error']}")
            
            else:
                print(f"   ❌ Error prefill: {prefill_result['error']}")
            
            self.results.append(result_entry)
            
            # Brief pause between requests
            import time
            time.sleep(2)
        
        return self.results
    
    def generate_report(self):
        """Generate comprehensive processing report"""
        print(f"\n📊 Generando reporte final...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Summary statistics
        total_orgs = len(self.results)
        successful_prefills = len([r for r in self.results if r['prefill_success']])
        successful_emails = len([r for r in self.results if r['email_success']])
        
        # Create report
        report = {
            'metadata': {
                'timestamp': timestamp,
                'form_id': self.form_id,
                'total_organizations_processed': total_orgs,
                'engine_version': '2.0'
            },
            'summary': {
                'successful_prefills': successful_prefills,
                'successful_emails': successful_emails,
                'failed_prefills': total_orgs - successful_prefills,
                'failed_emails': total_orgs - successful_emails,
                'success_rate_prefill': round(successful_prefills / total_orgs * 100, 1) if total_orgs > 0 else 0,
                'success_rate_email': round(successful_emails / total_orgs * 100, 1) if total_orgs > 0 else 0
            },
            'detailed_results': self.results,
            'configuration': {
                'clean_mapping_fields': len(self.clean_mapping),
                'excel_columns': len(self.excel_data.columns) if not self.excel_data.empty else 0
            }
        }
        
        # Save report
        try:
            filename = f"../outputs/PREFILL_ENGINE_V2_REPORT_{timestamp}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            # Also create Excel report
            excel_filename = f"../outputs/PREFILL_ENGINE_V2_REPORT_{timestamp}.xlsx"
            results_df = pd.DataFrame(self.results)
            results_df.to_excel(excel_filename, index=False)
            
            print(f"✅ Reporte JSON: {filename}")
            print(f"✅ Reporte Excel: {excel_filename}")
            
            return filename
            
        except Exception as e:
            print(f"❌ Error generando reporte: {e}")
            return None
    
    def run_complete_workflow(self):
        """Run complete prefill workflow"""
        print("=" * 70)
        print("🚀 PREFILL ENGINE V2.0 - SISTEMA COMPLETO SIN ERRORES")
        print("=" * 70)
        print(f"Formulario ID: {self.form_id}")
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Step 1: Load clean mapping
        if not self.load_clean_mapping():
            print("\n❌ No se pudo cargar mapeo limpio")
            return False
        
        # Step 2: Load Excel data
        if not self.load_excel_data():
            print("\n❌ No se pudieron cargar datos de Excel")
            return False
        
        # Step 3: Process all organizations
        results = self.process_all_organizations()
        
        # Step 4: Generate report
        report_file = self.generate_report()
        
        # Step 5: Final summary
        successful_prefills = len([r for r in results if r['prefill_success']])
        successful_emails = len([r for r in results if r['email_success']])
        
        print("\n" + "=" * 70)
        print("✅ PROCESAMIENTO COMPLETADO")
        print("=" * 70)
        print(f"📊 RESUMEN FINAL:")
        print(f"   • Total organizaciones: {len(results)}")
        print(f"   • Prefills exitosos: {successful_prefills}")
        print(f"   • Emails enviados: {successful_emails}")
        print(f"   • Tasa éxito prefill: {successful_prefills/len(results)*100:.1f}%")
        print(f"   • Tasa éxito email: {successful_emails/len(results)*100:.1f}%")
        
        if report_file:
            print(f"\n📁 Reportes generados en ../outputs/")
        
        print("=" * 70)
        
        return True

def main():
    """Main execution function"""
    engine = PrefillEngineV2()
    
    try:
        success = engine.run_complete_workflow()
        
        if success:
            print(f"\n🎉 ¡PREFILL ENGINE V2.0 EJECUTADO EXITOSAMENTE!")
        else:
            print(f"\n❌ Problemas en la ejecución")
            
    except KeyboardInterrupt:
        print("\n\n⏸️  Procesamiento cancelado por usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()