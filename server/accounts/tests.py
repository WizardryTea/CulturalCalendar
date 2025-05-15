# accounts/tests.py
from django.test import TestCase, Client
from django.urls import reverse, resolve
from accounts.models import CustomUser
from accounts.forms import CustomUserCreationForm, CustomAuthenticationForm
from accounts import views


class CustomUserModelTests(TestCase):
    def test_first_name_and_last_name_blank(self):
        user = CustomUser.objects.create(username='blankuser', email='blank@example.com')
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')

    def test_verbose_names(self):
        user = CustomUser(username='test', email='test@example.com')
        self.assertEqual(user._meta.get_field('username').verbose_name, 'Имя пользователя')
        self.assertEqual(user._meta.get_field('email').verbose_name, 'Электронная почта')
        self.assertEqual(user._meta.get_field('first_name').verbose_name, 'Имя')
        self.assertEqual(user._meta.get_field('last_name').verbose_name, 'Фамилия')

    def test_user_type_choices(self):
        choices = dict(CustomUser.USER_TYPE_CHOICES)
        self.assertIn(1, choices)
        self.assertIn(2, choices)
        self.assertEqual(choices[1], 'Администратор')
        self.assertEqual(choices[2], 'Пользователь')

    def test_db_table_and_verbose(self):
        self.assertEqual(CustomUser._meta.db_table, 'accounts_customuser')
        self.assertEqual(str(CustomUser._meta.verbose_name), 'Пользователь')
        self.assertEqual(str(CustomUser._meta.verbose_name_plural), 'Пользователи')

    def test_str_method_returns_username(self):
        user = CustomUser.objects.create(username='testuser', email='test@example.com')
        self.assertEqual(str(user), 'testuser')

    def test_save_updates_flags_on_change(self):
        user = CustomUser.objects.create(username='user1', email='user1@example.com', user_type=2)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        user.user_type = 1
        user.save()
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

class CustomUserCreationFormAdditionalTests(TestCase):
    def test_form_invalid_email_format(self):
        form_data = {
            'username': 'bademailuser',
            'email': 'not-an-email',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'user_type': 2
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_form_missing_required_fields(self):
        form_data = {
            'username': '',
            'email': '',
            'password1': '',
            'password2': '',
            'user_type': ''
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password1', form.errors)
        self.assertIn('password2', form.errors)

class CustomAuthenticationFormAdditionalTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='authuser2', email='authuser2@example.com', password='authpass123'
        )

    def test_auth_form_empty_data(self):
        form = CustomAuthenticationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('password', form.errors)

class AccountsViewsAdditionalTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='viewuser', email='viewuser@example.com', password='viewpass123', user_type=2
        )

    def test_signup_view_post_duplicate_username(self):
        data = {
            'username': 'viewuser',  # уже существует
            'email': 'newemail@example.com',
            'password1': 'Newpass123!',
            'password2': 'Newpass123!',
            'user_type': 2
        }
        response = self.client.post(reverse('accounts:signup'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertIn('username', response.context['form'].errors)

    def test_signup_view_post_duplicate_email(self):
        data = {
            'username': 'newuser',
            'email': 'viewuser@example.com',  # уже существует
            'password1': 'Newpass123!',
            'password2': 'Newpass123!',
            'user_type': 2
        }
        response = self.client.post(reverse('accounts:signup'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertIn('email', response.context['form'].errors)

    def test_login_view_post_wrong_password(self):
        data = {
            'username': 'viewuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('accounts:login'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)

    def test_logout_view_redirects_when_logged_in(self):
        self.client.login(username='viewuser', password='viewpass123')
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('affiche:index'))

    def test_logout_view_redirects_when_not_logged_in(self):
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('accounts:login'), response.url)

class CustomUserCreationFormsTests(TestCase):
    def test_form_labels_and_help_texts(self):
        form = CustomUserCreationForm()
        self.assertEqual(form.fields['username'].label, 'Имя пользователя')
        self.assertEqual(form.fields['email'].label, 'Электронная почта')
        self.assertEqual(form.fields['username'].help_text, 'Уникальное имя пользователя')
        self.assertEqual(form.fields['email'].help_text, 'На 1 почту можно зарегистрировать не более 1 аккаунта')

    def test_form_user_type_widget(self):
        form = CustomUserCreationForm()
        self.assertEqual(form.fields['user_type'].widget.__class__.__name__, 'RadioSelect')

    def test_form_save_sets_user_type(self):
        form_data = {
            'username': 'saveusertype',
            'email': 'saveusertype@example.com',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!',
            'user_type': 1
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.user_type, 1)


class CustomAuthenticationFormTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='authuser', email='authuser@example.com', password='authpass123'
        )

    def test_auth_form_valid(self):
        form = CustomAuthenticationForm(data={'username': 'authuser', 'password': 'authpass123'})
        self.assertTrue(form.is_valid())

    def test_auth_form_invalid(self):
        form = CustomAuthenticationForm(data={'username': 'authuser', 'password': 'wrongpass'})
        self.assertFalse(form.is_valid())

    def test_auth_form_labels(self):
        form = CustomAuthenticationForm()
        self.assertEqual(form.fields['username'].label, 'Имя пользователя')
        self.assertEqual(form.fields['password'].label, 'Пароль')


class AccountsViewsPostTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_view_post_success(self):
        data = {
            'username': 'signupuser',
            'email': 'signupuser@example.com',
            'password1': 'SignupPass123!',
            'password2': 'SignupPass123!',
            'user_type': 2
        }
        response = self.client.post(reverse('accounts:signup'), data)
        self.assertEqual(response.status_code, 302)  # редирект после успешной регистрации

    def test_signup_view_post_invalid(self):
        data = {
            'username': '',  # пустое имя пользователя
            'email': 'signupuser@example.com',
            'password1': 'SignupPass123!',
            'password2': 'SignupPass123!',
            'user_type': 2
        }
        response = self.client.post(reverse('accounts:signup'), data)
        self.assertEqual(response.status_code, 200)  # форма снова отображается
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

    def test_login_view_post_invalid(self):
        data = {
            'username': 'nouser',
            'password': 'nopass'
        }
        response = self.client.post(reverse('accounts:login'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

    def test_logout_view_without_login(self):
        response = self.client.get(reverse('accounts:logout'))
        # По умолчанию login_required редиректит на страницу логина
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login', response.url)


class AccountsUrlsTests(TestCase):
    def test_signup_url_resolves(self):
        url = reverse('accounts:signup')
        self.assertEqual(resolve(url).func, views.signup_view)

    def test_login_url_resolves(self):
        url = reverse('accounts:login')
        self.assertEqual(resolve(url).func, views.login_view)

    def test_logout_url_resolves(self):
        url = reverse('accounts:logout')
        self.assertEqual(resolve(url).func, views.logout_view)
