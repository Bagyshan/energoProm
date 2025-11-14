from import_export import resources, fields
from .models import HouseCard, Street, Address, Settlement
from user.models import User
from django.utils import timezone
from import_export.results import RowResult
from django.contrib.auth.hashers import make_password

class HouseCardImportResource(resources.ModelResource):
    house_card = fields.Field(attribute='house_card', column_name='Новый лицевой счет')
    old_house_card = fields.Field(attribute='old_house_card', column_name='Лицевой счет')
    full_name = fields.Field(column_name='Ф.И.О. абонента')
    street_name = fields.Field(column_name='Улица')
    house = fields.Field(column_name='Дом')
    liter = fields.Field(column_name='Литер')
    apartment = fields.Field(column_name='Кв.')
    apartment_liter = fields.Field(column_name='Литер кв.')
    
    class Meta:
        model = HouseCard
        import_id_fields = ('house_card',)
        fields = ('house_card', 'old_house_card', 'user', 'address')
        skip_unchanged = False
        report_skipped = True
    
    def before_import_row(self, row, **kwargs):
        """Валидация данных перед импортом строки"""
        # Пропускаем строки с заголовками
        if row.get('Лицевой счет') == 'Лицевой счет':
            raise ValueError("Пропуск строки заголовка")
        
        # Валидация обязательных полей
        required_fields = {
            'Новый лицевой счет': 'Новый лицевой счет',
            'Лицевой счет': 'Лицевой счет', 
            'Ф.И.О. абонента': 'Ф.И.О. абонента',
            'Улица': 'Улица'
        }
        
        for field_key, field_name in required_fields.items():
            value = row.get(field_key, '').strip()
            if not value:
                raise ValueError(f"Поле '{field_name}' обязательно")
        
        # Обработка пустых значений
        for key in ['Литер', 'Кв.', 'Литер кв.']:
            if key in row and (row[key] == '' or row[key] is None):
                row[key] = ''
    
    def init_instance(self, row=None):
        """Инициализация нового экземпляра с данными из строки"""
        if row is None:
            return self._meta.model()
        
        # Создаем экземпляр и сразу заполняем данными
        instance = self._meta.model()
        self._fill_instance(instance, row)
        return instance
    
    def _fill_instance(self, instance, row_data):
        """Заполняем экземпляр данными из строки"""
        # Сохраняем данные строки для использования при сохранении
        instance._row_data = row_data
        
        # Устанавливаем основные поля
        instance.house_card = str(row_data['Новый лицевой счет'])
        instance.old_house_card = str(row_data['Лицевой счет'])
        instance.contract_number = str(row_data['Новый лицевой счет'])
        instance.contract_date = timezone.now().date()
        instance.tp_number = 1
        instance.registered_at = timezone.now()
        instance.updated_at = timezone.now()
        instance.overpayment_underpayment = 0.0
        instance.penalty = 0.0
        instance.household_needs = 0.0
        instance.fact_summer = 0.0
        instance.fact_winter = 0.0
        instance.max_summer = 0.0
        instance.max_winter = 0.0
    
    def get_or_init_instance(self, instance_loader, row):
        """Правильная логика получения или инициализации экземпляра"""
        house_card = str(row.get('Новый лицевой счет', '').strip())
        
        if not house_card:
            raise ValueError("Новый лицевой счет не может быть пустым")
        
        try:
            # Пытаемся найти существующую запись
            instance = HouseCard.objects.get(house_card=house_card)
            self._fill_instance(instance, row)  # Обновляем данные
            return instance, False
        except HouseCard.DoesNotExist:
            # Создаем новую запись
            instance = self.init_instance(row)
            return instance, True
    
    def save_instance(self, instance, is_create, row, **kwargs):
        """Создаем связанные объекты и сохраняем"""
        if hasattr(instance, '_row_data'):
            self._create_related_objects(instance, instance._row_data)
        
        super().save_instance(instance, is_create, row, **kwargs)
    
    def _create_related_objects(self, house_card_instance, row_data):
        """Создаем пользователя, адрес и другие связанные объекты"""
        # Получаем или создаем населенный пункт по умолчанию
        settlement, _ = Settlement.objects.get_or_create(
            name="Основной населенный пункт",
            defaults={
                'created_at': timezone.now(),
                'updated_at': timezone.now()
            }
        )
        
        # Получаем или создаем улицу
        street_name = row_data.get('Улица', '').strip()
        street, _ = Street.objects.get_or_create(
            name=street_name,
            settlement=settlement,
            defaults={
                'created_at': timezone.now(),
                'updated_at': timezone.now()
            }
        )
        
        # Создаем адрес
        house_number = str(row_data.get('Дом', '0')).strip()
        liter = str(row_data.get('Литер', '')).strip()
        apartment = row_data.get('Кв.', '')
        apartment_liter = str(row_data.get('Литер кв.', '')).strip()
        
        # Преобразуем квартиру в число, если возможно
        # apartment_int = None
        # if apartment and str(apartment).strip().isdigit():
        #     apartment_int = int(apartment)
        
        # address = Address.objects.create(
        #     house=house_number,
        #     liter=liter,
        #     apartment=apartment_int,
        #     apartment_liter=apartment_liter,
        #     street=street,
        #     created_at=timezone.now(),
        #     updated_at=timezone.now()
        # )
        apartment_str = str(row_data.get('Кв.', '')).strip()
        address = Address.objects.create(
            house=house_number,
            liter=liter,
            apartment=apartment_str,  # Сохраняем как строку
            apartment_liter=apartment_liter,
            street=street,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        
        # Создаем пользователя
        full_name = row_data.get('Ф.И.О. абонента', '').strip()
        house_card_number = str(row_data['Новый лицевой счет'])
        password_hash = make_password(
            house_card_number, 
            salt='xBdXoOjCOYB7rkl7S0x8um',  # Используем тот же salt для консистентности
            hasher='pbkdf2_sha256'
        )
        
        user = User.objects.create(
            name=full_name,
            email=f"{row_data['Новый лицевой счет']}@energoprom.com",
            password=password_hash,
            registered_at=timezone.now(),
            updated_at=timezone.now(),
            is_active=True,
            is_staff=False,
            is_superuser=False,
            is_verified_email=True
        )
        
        # Устанавливаем связи
        house_card_instance.user = user
        house_card_instance.address = address
    
    def after_import_row(self, row, row_result, **kwargs):
        """Очистка временных данных после импорта строки"""
        if hasattr(row_result.instance, '_row_data'):
            delattr(row_result.instance, '_row_data')