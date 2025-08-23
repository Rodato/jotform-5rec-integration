"""
Prefill Engine v2.0 - Motor de prefill optimizado sin errores
Sistema completo de prefill con mapeo limpio, validación y emails
"""

import pandas as pd
import requests
import smtplib
import json
import base64
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from pathlib import Path
from config import JOTFORM_API_KEY, FORM_ID, GMAIL_USER, GMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT, FROM_NAME
from excel_generator import ExcelPrefillGenerator

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
        
        # Excel generator for output
        self.excel_generator = ExcelPrefillGenerator()
        
    def load_clean_mapping(self):
        """Load validated clean mapping"""
        print("🗺️  Cargando mapeo limpio validado...")
        
        try:
            # Find latest mapping files (try different formats)
            outputs_dir = Path("../outputs")
            
            # First try to find SIMPLE_MAPPING files
            mapping_files = list(outputs_dir.glob("SIMPLE_MAPPING_*.json"))
            
            if mapping_files:
                latest_mapping = max(mapping_files, key=lambda x: x.stat().st_mtime)
                
                with open(latest_mapping, 'r', encoding='utf-8') as f:
                    self.clean_mapping = json.load(f)
                
                print(f"✅ Mapeo cargado: {len(self.clean_mapping)} campos")
                print(f"   Archivo: {latest_mapping.name}")
                return True
            
            # If no SIMPLE_MAPPING, try FORM_COMPLETE files
            complete_files = list(outputs_dir.glob("FORM_COMPLETE_*.json"))
            
            if complete_files:
                latest_complete = max(complete_files, key=lambda x: x.stat().st_mtime)
                
                with open(latest_complete, 'r', encoding='utf-8') as f:
                    form_data = json.load(f)
                
                # Extract field mapping from complete form data
                self.clean_mapping = {}
                questions = form_data.get('questions', {})
                
                for qid, question in questions.items():
                    # Skip non-input fields
                    field_type = question.get('type', '')
                    if field_type in ['control_head', 'control_pagebreak', 'control_button', 'control_fileupload']:
                        continue
                    
                    # Use field name or text as mapping key
                    field_name = question.get('name', '')
                    field_text = question.get('text', '')
                    
                    if field_name:
                        # Use field name as key for mapping
                        self.clean_mapping[field_name] = qid
                    elif field_text:
                        # Use field text as key (clean it) - sin limitar longitud
                        clean_text = field_text.replace('\n', ' ').strip()
                        self.clean_mapping[clean_text] = qid
                
                print(f"✅ Mapeo generado desde datos completos: {len(self.clean_mapping)} campos")
                print(f"   Archivo: {latest_complete.name}")
                print(f"   Campos mapeables: {list(self.clean_mapping.keys())[:5]}...")
                return True
            
            print("❌ No se encontraron archivos de mapeo (SIMPLE_MAPPING o FORM_COMPLETE)")
            return False
                
        except Exception as e:
            print(f"❌ Error cargando mapeo: {e}")
            return False
    
    def find_excel_files(self):
        """Find all Excel files in inputs directory"""
        inputs_dir = Path("../inputs")
        if not inputs_dir.exists():
            print("❌ Directorio ../inputs no existe")
            return []
        
        excel_files = list(inputs_dir.glob("*.xlsx"))
        return [f for f in excel_files if not f.name.startswith('~')]  # Exclude temp files
    
    def select_excel_file(self):
        """Select Excel file to process"""
        excel_files = self.find_excel_files()
        
        if not excel_files:
            print("❌ No se encontraron archivos .xlsx en la carpeta inputs/")
            return None
        
        if len(excel_files) == 1:
            selected_file = excel_files[0]
            print(f"📊 Archivo Excel detectado: {selected_file.name}")
            return selected_file
        
        # Multiple files - let user choose
        print(f"📊 Se encontraron {len(excel_files)} archivos Excel:")
        for i, file in enumerate(excel_files, 1):
            print(f"   {i}. {file.name}")
        
        while True:
            try:
                choice = input("\nSelecciona el archivo a procesar (número): ").strip()
                if not choice:
                    # Default to first file if no input
                    selected_file = excel_files[0]
                    print(f"   Usando archivo por defecto: {selected_file.name}")
                    return selected_file
                
                index = int(choice) - 1
                if 0 <= index < len(excel_files):
                    selected_file = excel_files[index]
                    print(f"   Archivo seleccionado: {selected_file.name}")
                    return selected_file
                else:
                    print(f"   ❌ Número inválido. Debe ser entre 1 y {len(excel_files)}")
            except (ValueError, KeyboardInterrupt, EOFError):
                # Handle non-interactive environments
                selected_file = excel_files[0]
                print(f"   🤖 Modo automático: usando {selected_file.name}")
                return selected_file

    def load_excel_data(self, excel_path=None):
        """Load and validate Excel data"""
        if excel_path is None:
            excel_file = self.select_excel_file()
            if excel_file is None:
                return False
            excel_path = excel_file
        
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
    
    def load_image_as_base64(self, image_path):
        """Load image and convert to base64 for inline embedding"""
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
                return base64.b64encode(image_data).decode('utf-8')
        except Exception as e:
            print(f"⚠️  Error cargando imagen {image_path}: {e}")
            return None
    
    def send_email(self, to_email, empresa, edit_url, mapped_fields):
        """Send email with prefilled form URL"""
        
        # Create email content (original structure with CID images)
        subject = f"Formulario 5REC Pre-llenado - {empresa}"
        
        html_body = f"""
        <html>
        <head></head>
        <body>
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                
                <!-- Header Image -->
                <div style="text-align: center; margin-bottom: 20px;">
                    <img src="cid:header_image" style="width: 100%; max-width: 600px; height: auto; display: block; margin: 0 auto;" alt="5REC Header">
                </div>
                
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
                        <div style="text-align: center; margin: 15px 0;">
                            <a href="{edit_url}" style="text-decoration: none; display: inline-block;">
                                <img src="cid:button_image" style="max-width: 200px; height: auto; border: none;" alt="Acceder al Formulario 5REC">
                            </a>
                        </div>
                        <div style="text-align: center; margin-top: 10px;">
                            <a href="{edit_url}" 
                               style="display: inline-block; background-color: #2c5aa0; color: white; 
                                      padding: 12px 25px; text-decoration: none; border-radius: 5px; 
                                      font-weight: bold;">
                                ▶️ Abrir Formulario Pre-llenado
                            </a>
                        </div>
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
            # Create message with related content for embedded images
            message = MIMEMultipart("related")
            message["Subject"] = subject
            message["From"] = f"{FROM_NAME} <{self.email_config['email_user']}>"
            message["To"] = to_email
            
            # Create alternative container for HTML content
            msg_alternative = MIMEMultipart("alternative")
            
            # Add HTML content
            html_part = MIMEText(html_body, "html")
            msg_alternative.attach(html_part)
            
            # Attach the alternative container to main message
            message.attach(msg_alternative)
            
            # Load and attach images with Content-ID
            header_img_path = Path("../img/5REC Franja.png")
            button_img_path = Path("../img/Imagen 5REC formulario.png")
            
            # Attach header image
            if header_img_path.exists():
                with open(header_img_path, 'rb') as f:
                    img_data = f.read()
                    img = MIMEImage(img_data)
                    img.add_header('Content-ID', '<header_image>')
                    img.add_header('Content-Disposition', 'inline', filename='5REC_Franja.png')
                    message.attach(img)
            
            # Attach button image  
            if button_img_path.exists():
                with open(button_img_path, 'rb') as f:
                    img_data = f.read()
                    img = MIMEImage(img_data)
                    img.add_header('Content-ID', '<button_image>')
                    img.add_header('Content-Disposition', 'inline', filename='Imagen_5REC_formulario.png')
                    message.attach(img)
            
            # Send email
            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.starttls()
                server.login(self.email_config['email_user'], self.email_config['email_password'])
                server.send_message(message)
            
            return {'success': True, 'error': None}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def process_all_organizations(self, send_emails=False):
        """Process all organizations in Excel data"""
        print(f"\n🚀 Procesando {len(self.excel_data)} organizaciones...")
        print(f"📧 Modo envío de emails: {'ACTIVADO' if send_emails else 'DESACTIVADO - Solo generando tabla Excel'}")
        
        for idx, row in self.excel_data.iterrows():
            print(f"\n📋 Procesando organización {idx + 1}/{len(self.excel_data)}")
            
            # Get organization details
            empresa = row.get('Nombre Empresa/Organización', f'Organización_{idx}')
            email_destinatario = row.get('Email Destinatario', '')
            
            print(f"   🏢 Empresa: {empresa}")
            print(f"   📧 Email: {email_destinatario}")
            
            # Process even without email for Excel generation
            if pd.isna(email_destinatario) or not email_destinatario.strip():
                print(f"   ⚠️  Sin email - procesando solo para tabla")
                email_destinatario = 'Sin email'
            
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
                
                # Send email only if requested and email is valid
                if send_emails and email_destinatario != 'Sin email':
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
                    print(f"   📊 Guardando para tabla Excel")
            
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
    
    def run_complete_workflow(self, send_emails=False, generate_excel=True):
        """Run complete prefill workflow"""
        print("=" * 70)
        print("🚀 PREFILL ENGINE V2.0 - SISTEMA COMPLETO CON EXCEL")
        print("=" * 70)
        print(f"Formulario ID: {self.form_id}")
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📧 Envío de emails: {'ACTIVADO' if send_emails else 'DESACTIVADO'}")
        print(f"📊 Generación Excel: {'ACTIVADO' if generate_excel else 'DESACTIVADO'}")
        
        # Step 1: Load clean mapping
        if not self.load_clean_mapping():
            print("\n❌ No se pudo cargar mapeo limpio")
            return False
        
        # Step 2: Load Excel data
        if not self.load_excel_data():
            print("\n❌ No se pudieron cargar datos de Excel")
            return False
        
        # Step 3: Process all organizations
        results = self.process_all_organizations(send_emails=send_emails)
        
        # Step 4: Generate reports
        report_file = self.generate_report()
        
        # Step 5: Generate Excel table if requested
        excel_file = None
        if generate_excel:
            print(f"\n📊 Generando tabla Excel con links de prefill...")
            excel_file = self.excel_generator.generate_prefill_excel(results, self.form_id)
            
            # Also generate email templates
            template_file = self.excel_generator.generate_email_templates_file(results)
            print(f"📝 Templates de email: {template_file}")
        
        # Step 6: Final summary
        successful_prefills = len([r for r in results if r['prefill_success']])
        successful_emails = len([r for r in results if r['email_success']])
        
        print("\n" + "=" * 70)
        print("✅ PROCESAMIENTO COMPLETADO")
        print("=" * 70)
        print(f"📊 RESUMEN FINAL:")
        print(f"   • Total organizaciones: {len(results)}")
        print(f"   • Prefills exitosos: {successful_prefills}")
        
        if send_emails:
            print(f"   • Emails enviados: {successful_emails}")
            print(f"   • Tasa éxito email: {successful_emails/len(results)*100:.1f}%")
        
        print(f"   • Tasa éxito prefill: {successful_prefills/len(results)*100:.1f}%")
        
        if report_file:
            print(f"\n📁 Reportes JSON generados en ../outputs/")
        
        if excel_file:
            print(f"📊 Tabla Excel con links: {excel_file.name}")
            print(f"💡 Usar la tabla Excel para enviar emails manualmente")
        
        print("=" * 70)
        
        return True

def main():
    """Main execution function"""
    engine = PrefillEngineV2()
    
    try:
        print("\n🔧 CONFIGURACIÓN DE EJECUCIÓN:")
        print("1. Solo generar Excel (recomendado)")
        print("2. Generar Excel + enviar emails")
        
        try:
            mode = input("\nSelecciona modo (1 o 2, Enter para modo 1): ").strip()
        except (KeyboardInterrupt, EOFError):
            mode = "1"  # Default for non-interactive
        
        if mode == "2":
            send_emails = True
            print("📧 Modo: Generando Excel Y enviando emails")
        else:
            send_emails = False
            print("📊 Modo: Solo generando Excel (sin envío de emails)")
        
        success = engine.run_complete_workflow(send_emails=send_emails, generate_excel=True)
        
        if success:
            print(f"\n🎉 ¡PREFILL ENGINE V2.0 EJECUTADO EXITOSAMENTE!")
            if not send_emails:
                print(f"💡 Revisa la tabla Excel generada para copiar links de prefill")
        else:
            print(f"\n❌ Problemas en la ejecución")
            
    except KeyboardInterrupt:
        print("\n\n⏸️  Procesamiento cancelado por usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()