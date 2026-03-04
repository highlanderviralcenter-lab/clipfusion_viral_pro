"""ClipFusion — Secondary Group Strategy. Expansão para público secundário."""


class SecondaryGroupStrategy:

    def dual_hook(self, hook: str, primary: str, secondary: dict) -> str:
        """Enriquece o gancho para atrair também o grupo secundário."""
        angle = secondary.get("angulo_gancho", "")
        if angle:
            return f"{hook} ({angle})"
        return hook

    def expansion_report(self, primary: str, secondary: dict) -> str:
        return (f"Público primário: {primary}\n"
                f"Expansão: {secondary.get('nome', '')} "
                f"(+{secondary.get('expansao_potencial', '?')} alcance estimado)")
