import flet as ft
import string
import secrets
from zxcvbn import zxcvbn

def main(page: ft.Page):
    # Configurações da Janela
    page.title = "Gerador de Senhas Seguro"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.theme_mode = "dark" 
    page.window_width = 400
    page.window_height = 700
    page.scroll = "adaptive"

    # Elementos da UI
    title = ft.Text("Gerador de Senhas", size=30, weight="bold")
    subtitle = ft.Text("Nível: Personalizado", size=14, color="grey")

    txt_password = ft.TextField(
        value="",
        text_align="center",
        width=300,
        read_only=True,
        text_style=ft.TextStyle(size=20, weight="bold"),
        border_color="blue",
    )

    strength_bar = ft.ProgressBar(width=300, value=0, color="red")
    strength_text = ft.Text("Força da senha: N/A", size=12)

    lbl_length = ft.Text("Comprimento: 12", size=16)
    slider_length = ft.Slider(
        min=4, max=32, divisions=28, value=12, label="{value}", width=300
    )

    chk_upper = ft.Checkbox(label="Incluir Letras Maiúsculas", value=True)
    chk_lower = ft.Checkbox(label="Incluir Letras Minúsculas", value=True)
    chk_numbers = ft.Checkbox(label="Incluir Números", value=True)
    chk_symbols = ft.Checkbox(label="Incluir Símbolos", value=False)

    # Lógica
    def update_strength(password):
        if not password:
            strength_bar.value = 0
            strength_text.value = "Força da senha: N/A"
            strength_bar.color = "grey"
            return

        result = zxcvbn(password)
        score = result['score']
        
        strength_bar.value = (score + 1) / 5
        
        msgs = ["Muito Fraca", "Fraca", "Razoável", "Forte", "Muito Forte"]
        # Cores em texto simples
        cols = ["red", "orange", "yellow", "green", "blue"]
        
        strength_text.value = f"Força: {msgs[score]}"
        strength_text.color = cols[score]
        strength_bar.color = cols[score]
        page.update()

    def generate_password(e):
        length = int(slider_length.value)
        chars = ""
        if chk_upper.value: chars += string.ascii_uppercase
        if chk_lower.value: chars += string.ascii_lowercase
        if chk_numbers.value: chars += string.digits
        if chk_symbols.value: chars += string.punctuation

        if not chars:
            txt_password.value = "Selecione uma opção!"
            page.update()
            return

        password = ''.join(secrets.choice(chars) for _ in range(length))
        txt_password.value = password
        update_strength(password)
        page.update()

    def copy_to_clipboard(e):
        page.set_clipboard(txt_password.value)
        page.snack_bar = ft.SnackBar(ft.Text("Senha copiada!"), open=True)
        page.update()

    def on_slider_change(e):
        lbl_length.value = f"Comprimento: {int(slider_length.value)}"
        page.update()

    slider_length.on_change = on_slider_change
    
    btn_generate = ft.ElevatedButton("Gerar Senha", on_click=generate_password, width=300, height=50)
    btn_copy = ft.OutlinedButton("Copiar", on_click=copy_to_clipboard, width=300)

    page.add(
        ft.Column(
            [title, subtitle, ft.Divider(), lbl_length, slider_length, 
             chk_upper, chk_lower, chk_numbers, chk_symbols, 
             ft.Divider(), btn_generate, ft.Divider(height=10), 
             txt_password, strength_bar, strength_text, 
             ft.Divider(height=10), btn_copy],
            alignment="center",
            horizontal_alignment="center",
        )
    )

ft.app(target=main)