import json

from textual import screen, widgets, app, on, containers
from textual.binding import Binding

from module_manager import ModuleManager, Module

module_manager = ModuleManager()


class OptionsEdit(widgets.Static):
    def compose(self) -> app.ComposeResult:
        self.text_area = widgets.TextArea(text="Модуль не выбран", language="json", disabled=True,
                                          show_line_numbers=True)
        self.turn_on_swich = widgets.Switch(value=False, disabled=True, animate=False)
        self.turn_on_label = widgets.Label("\nАктивен\n")
        self.version_label = widgets.TextArea(text="Вер. \n", disabled=True)

        self.text_area.styles.width = "3fr"

        with containers.Horizontal(id="plugin_container"):
            with containers.Vertical(id="ver_switch") as left_menu:
                left_menu.styles.width = "1fr"
                yield self.version_label
                with containers.Horizontal(id="turn_on_swich") as swicher:
                    swicher.styles.height = "3fr"
                    yield self.turn_on_label
                    yield self.turn_on_swich
            yield self.text_area

    def from_option(self, option_name):
        module_manager.init_module(option_name)
        self.module: Module = module_manager.modules[option_name]
        self.version_label.text = f"Версия: {self.module.settings.version}\n"
        self.turn_on_swich.disabled = False
        self.turn_on_swich.value = self.module.settings.is_active

        self.text_area.text = json.dumps(self.module.settings.config, indent=2, ensure_ascii=False)
        self.text_area.disabled = False
        self.update()

    def action_save(self):
        self.module.settings.is_active = self.turn_on_swich.value
        self.module.settings.config = json.loads(self.text_area.text)
        self.module.save_settings()

    # @on(widgets.TextArea.Changed)
    # def on_change_text(self, event: widgets.TextArea.Changed):
    #     self.text_area.border_title = "*"


class ModulesScreen(screen.Screen):
    BINDINGS = [
        ("escape", "app.pop_screen", "back"),
        ("ctrl+s", "save", "save")
    ]
    TITLE = "Modules"

    def compose(self) -> app.ComposeResult:
        yield widgets.Header()
        yield widgets.Footer()

        yield widgets.Select(
            [(module, module) for module in module_manager.name_list],
            prompt="Выберите модуль"
        )
        self.option_layout = OptionsEdit(classes="box")
        yield self.option_layout

    @on(widgets.Select.Changed)
    def select_changed(self, event: widgets.Select.Changed) -> None:
        self.title = str(event.value)
        self.option_layout.from_option(str(event.value))

    def action_save(self):
        self.option_layout.action_save()
