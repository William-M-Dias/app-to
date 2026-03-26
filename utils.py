import os
import cloudinary
import cloudinary.uploader

# Configuração automática usando as variáveis que você definiu no Group Env do Render
cloudinary.config( 
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'), 
    api_key = os.getenv('CLOUDINARY_API_KEY'), 
    api_secret = os.getenv('CLOUDINARY_API_SECRET'),
    secure = True
)

def upload_foto_paciente(arquivo_imagem):
    """
    Envia a foto para o Cloudinary com transformações Clean & Calm.
    Retorna a URL segura (https) ou None em caso de falha.
    """
    try:
        if not arquivo_imagem:
            return None

        # O Cloudinary usa IA para detectar o rosto (gravity: face) 
        # e aplicar o arredondamento (radius: 20) solicitado.
        upload_result = cloudinary.uploader.upload(
            arquivo_imagem,
            folder="app_to/pacientes",
            transformation=[
                {'width': 400, 'height': 400, 'crop': 'fill', 'gravity': 'face'},
                {'fetch_format': 'auto', 'quality': 'auto'},
                {'radius': 20} 
            ]
        )
        return upload_result.get('secure_url')
    except Exception as e:
        print(f"Erro Crítico no Cloudinary: {e}")
        return None