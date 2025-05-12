import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import getpass

def enviar_email_html(remetente, senha, destinatarios, assunto,
                      cc=None, arquivo_html="index.html", smtp_server="email-ssl.com.br", smtp_port=465):
    cc = cc or []  # Garante que seja uma lista

    # Lê o conteúdo HTML
    with open(arquivo_html, 'r', encoding='utf-8') as f:
        conteudo_html = f.read()

    # Monta o e-mail
    mensagem = MIMEMultipart("alternative")
    mensagem["From"] = remetente
    mensagem["To"] = ", ".join(destinatarios)
    if cc:
        mensagem["Cc"] = ", ".join(cc)
    mensagem["Subject"] = assunto

    parte_html = MIMEText(conteudo_html, "html")
    mensagem.attach(parte_html)

    # Envia o e-mail para destinatários + CC
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as servidor:
            servidor.login(remetente, senha)
            all_recipients = destinatarios + cc
            servidor.sendmail(remetente, all_recipients, mensagem.as_string())
        print("✅ E-mail enviado com sucesso!")
    except Exception as e:
        print("❌ Erro ao enviar o e-mail:", e)

# Execução
if __name__ == "__main__":
    if len(sys.argv) == 8:
        _, remetente, lista_destinatarios, lista_cc, assunto, arquivo_html, smtp_server, smtp_port = sys.argv
        senha = getpass.getpass("Digite sua senha de e-mail (não será exibida): ")
        destinatarios = [email.strip() for email in lista_destinatarios.split(",") if email.strip()]
        cc = [email.strip() for email in lista_cc.split(",") if email.strip()]
    else:
        remetente = input("E-mail remetente: ")
        senha = getpass.getpass("Senha do e-mail: ")
        lista_destinatarios = input("Destinatários (separados por vírgula): ")
        lista_cc = input("CC (separados por vírgula) [opcional]: ")
        assunto = input("Assunto: ") or "Assunto padrão"
        arquivo_html = input("Arquivo HTML [index.html]: ") or "index.html"
        smtp_server = input("Servidor SMTP [email-ssl.com.br]: ") or "email-ssl.com.br"
        smtp_port = input("Porta SMTP [465]: ") or "465"

        destinatarios = [email.strip() for email in lista_destinatarios.split(",") if email.strip()]
        cc = [email.strip() for email in lista_cc.split(",") if email.strip()]

    enviar_email_html(remetente, senha, destinatarios, assunto,
                      cc, arquivo_html, smtp_server, int(smtp_port))