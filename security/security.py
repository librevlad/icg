from contracts.contract import Contract

class SecurityLayer:
    def validate(self, contract: Contract) -> bool:
        return True  # MVP
