- 21.04.2022 Михаил Краснов <linuxoid85@gmail.com>
	- Изменение логики `cp_info.format_out.base_info()` - теперь не требуется
	  передавать кортеж с нужными параметрами. Все данные берутся из конфига
	  порта - секции `['package']`

- 20.04.2022 Михаил Краснов <linuxoid85@gmail.com>
	- **Конфигурация:**
		- Добавление параметров `sbu` и `[remove]allow_rem_of_system_ports`
	- **`cp_default.py`:**
		- Мелкий фикс `msg.log()`;
	- **`cp_info.py`:**
		- Изменение логики `format_out.base_info()`;
		- Добавление метода `format_out.deps_info()`;
		- Изменение поведения `format_out.description()`:
			- Полное описание теперь выводится через строку от краткого.

- 17.04.2022 Михаил Краснов <linuxoid85@gmail.com>
	- Унификация использования классов API;
	- Добавление модуля `cp_remove`;

- 16.04.2022 Михаил Краснов <linuxoid85@gmail.com>
	- Initial commit
