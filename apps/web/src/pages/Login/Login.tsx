
import { LockOutlined, UserOutlined } from '@ant-design/icons';
import { Button, Flex, Form, Input, message } from 'antd';
import { useEffect, useState } from 'react';
import { useDispatch } from 'react-redux';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { fetchGetUserMe, fetchLogin } from '../../api/login';
import { setUser } from '../../store/features/user/slice';
import logo from "./../../assets/logo.png";
import styles from './Login.module.scss';

const onFinishFailed = (errorInfo: any) => {
    console.log('Failed:', errorInfo);
};

const Login: React.FC = () => {
    const [loading, setLoading] = useState(false);
    const dispatch = useDispatch();
    const [messageApi, contextHolder] = message.useMessage({ duration: 5 });
    const navigate = useNavigate();
    const [searchParams, setSearchParams] = useSearchParams();
    const callback_url = searchParams.get('callback_url') ? searchParams.get('callback_url')?.toString() : '/info_system';

    const success = () => {
        messageApi.open({
            type: 'success',
            content: 'Вход прошел успешно',
        });
    };

    const error = () => {
        messageApi.open({
            type: 'error',
            content: 'При попытке входа произошла ошибка. Проверьте правильность почты и пароля',
        });
    };

    const checkMe = async () => {
        const { data, isError } = await fetchGetUserMe()
        if (isError) {
            console.error('Me error');
            return;
        }
        dispatch(setUser(data));
        if (callback_url) {
            navigate(callback_url);
        }
    }


    const onFinish = async (values: any) => {
        setLoading(true);
        const { data, isError } = await fetchLogin(values);
        if (isError) {
            error();
            setLoading(false);
            return;
        }
        localStorage.setItem('accessToken', data.access_token);
        setLoading(false);
        success();
        if (callback_url) {
            navigate(callback_url);
        }
    };

    useEffect(() => {
        checkMe();
    }, [loading]);



    return (
        <div className={styles.container}>
            <div className={styles.formContainer}>
                <Flex vertical align='center' style={{ margin: '32px' }}>
                    <img src={logo} alt='' width='128px' />
                    <div className={styles.caption} style={{ textAlign: 'center' }}>
                        ФОРПОСТ
                    </div>
                </Flex>

                <Form
                    name='login'
                    labelCol={{ span: 8 }}
                    wrapperCol={{ span: 16 }}
                    style={{ maxWidth: 600, margin: 'auto' }}
                    initialValues={{ remember: true }}
                    onFinish={onFinish}
                    onFinishFailed={onFinishFailed}
                    autoComplete='off'
                >
                    {contextHolder}
                    <Form.Item
                        name='username'
                        rules={[{ required: true, message: 'Пожалуйста, укажите адрес почты' }]}
                    >
                        <Input
                            placeholder="Электронная почта"
                            prefix={<UserOutlined className="site-form-item-icon" />}
                            style={{ width: '300px', alignItems: 'center' }}
                        />
                    </Form.Item>

                    <Form.Item
                        name='password'
                        rules={[{ required: true, message: 'Пожалуйста, введите пароль' }]}
                    >
                        <Input.Password
                            type='password'
                            placeholder="Пароль"
                            prefix={<LockOutlined className="site-form-item-icon" />}
                            style={{ width: '300px', alignItems: 'center' }}
                        />
                    </Form.Item>

                    <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
                        <Button type='primary' htmlType='submit' loading={loading}>
                            Войти
                        </Button>
                    </Form.Item>
                </Form>
            </div>
        </div>)
}
export default Login