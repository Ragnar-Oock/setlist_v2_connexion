from connexion.resolver import RestyResolver


class FixedRestyResolver(RestyResolver):
    def resolve_function_from_operation_id(self, operation_id):
        operation_id = self.default_module_name + "." + operation_id
        return super().resolve_function_from_operation_id(operation_id)
