# """Config Flow for Oura Ring HA integration."""
# from __future__ import annotations

# from typing import Any

# import voluptuous as vol

# from homeassistant import config_entries
# from homeassistant.data_entry_flow import FlowResult
# from homeassistant.const import CONF_API_TOKEN
# from .const import DOMAIN


# OURA_SCHEMA = vol.Schema(
#     {
#         vol.Required(CONF_API_TOKEN): str,
#     }
# )

# class OuraConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
#     """Handle a config flow for Oura_Ring_HA"""
#     async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
#         """Handle the initial step"""
#         if user_input is not None:
#             data = user_input["api_token"]
#             await self.async_set_unique_id(data)
#             self._abort_if_unique_id_configured()
#             return self.async_create_entry(title="Oura Ring HA",data=data,)

#         return self.async_show_form(step_id="user", data_schema=OURA_SCHEMA)
