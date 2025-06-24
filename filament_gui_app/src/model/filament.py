class Filament:
    def __init__(self, data):
        self.brand = data.get('brand', 'Unknown')
        self.color = data.get('color', 'Unknown')
        self.material = data.get('material', 'Unknown')
        self.weight = data.get('weight', 0.0)
        self.purchase_link = data.get('purchase_link', '')
        self.cost = data.get('cost', 0.0)
        self.RGB_color = data.get('RGB_color', None)
        self.k_factor = data.get("k_factor", 0.0)
        self.flow_rate = data.get("flow_rate", 0.0)  # New field

    @property
    def cost_per_kg(self):
        """Calculate and return the cost per kilogram."""
        if self.weight > 0:
            return self.cost / self.weight  # cost per kg
        return 0

    def __str__(self):
        return (
            f"Filament(brand={self.brand}, color={self.color}, material={self.material}, "
            f"weight={self.weight}, purchase_link={self.purchase_link}, cost={self.cost}, "
            f"RGB_color={self.RGB_color}, k_factor={self.k_factor}, flow_rate={self.flow_rate})"
        )