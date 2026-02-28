import flet

class EmployeeApp:
    def __init__(self, page: flet.Page):
        self.page = page
        self.page.title = "Каталог сотрудников"
        self.page.window_width = 500
        self.page.window_height = 800
        self.employees = []
        self.build_ui()

    def build_ui(self):
        self.first_name = flet.TextField(label="Имя")
        self.last_name = flet.TextField(label="Фамилия")
        self.age = flet.TextField(label="Возраст", keyboard_type=flet.KeyboardType.NUMBER)
        self.salary = flet.TextField(label="Зарплата", keyboard_type=flet.KeyboardType.NUMBER)
        
        self.position = flet.Dropdown(
            label="Должность",
            options=[
                flet.dropdown.Option("Разработчик"),
                flet.dropdown.Option("Дизайнер"),
                flet.dropdown.Option("Менеджер"),
                flet.dropdown.Option("Тестировщик"),
            ]
        )

        self.error_text = flet.Text(color="red")
        self.employee_list = flet.Column()

        add_button = flet.FilledButton(
            "Добавить сотрудника", 
            on_click=self.add_employee
        )

        self.page.add(
            flet.Text("Ввод данных", size=20, weight="bold"),
            self.first_name,
            self.last_name,
            self.age,
            self.position,
            self.salary,
            self.error_text,
            add_button,
            flet.Divider(),
            flet.Text("Список сотрудников", size=20, weight="bold"),
            flet.ListView(controls=[self.employee_list], expand=True)
        )

    def add_employee(self, e):
        if not all([self.first_name.value, self.last_name.value, self.age.value, self.position.value, self.salary.value]):
            self.error_text.value = "Заполните все поля"
            self.page.update()
            return

        try:
            age_val = int(self.age.value)
            salary_val = float(self.salary.value)
        except ValueError:
            self.error_text.value = "Возраст и зарплата — числа"
            self.page.update()
            return

        new_emp = {
            "name": f"{self.first_name.value} {self.last_name.value}",
            "age": age_val,
            "pos": self.position.value,
            "salary": salary_val
        }

        self.employees.append(new_emp)
        self.employees.sort(key=lambda x: x["salary"])
        self.error_text.value = ""
        
        self.first_name.value = ""
        self.last_name.value = ""
        self.age.value = ""
        self.salary.value = ""
        self.position.value = None
        
        self.update_list()

    def delete_employee(self, emp):
        self.employees.remove(emp)
        self.update_list()

    def update_list(self):
        self.employee_list.controls.clear()
        for emp in self.employees:
            is_high = emp["salary"] > 100000
            
            row = flet.Container(
                content=flet.Row([
                    flet.Column([
                        flet.Text(emp["name"], weight="bold"),
                        flet.Text(f"{emp['pos']} | {emp['age']} лет | {emp['salary']}"),
                    ], expand=True),
                    flet.IconButton(
                        icon=flet.Icons.DELETE_OUTLINE, 
                        on_click=lambda _, i=emp: self.delete_employee(i)
                    )
                ]),
                padding=10,
                border_radius=5,
                bgcolor=flet.Colors.YELLOW_100 if is_high else None,
                border=flet.border.all(1, flet.Colors.GREY_300)
            )
            self.employee_list.controls.append(row)
        self.page.update()

def main(page: flet.Page):
    EmployeeApp(page)

if __name__ == "__main__":
    flet.app(target=main)