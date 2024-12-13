import { Button, Flex, Layout, Menu, Typography } from 'antd';
import React, { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { Link, Outlet, useLocation, useNavigate } from 'react-router-dom';
import { fetchGetUserMe } from './api/login';
import logo from './assets/logo_white.png';
import { useAppSelector } from './hooks/useAppSelector';
import { setUser } from './store/features/user/slice';
const { Content, Footer, Header } = Layout;




const Main: React.FC = () => {
	const user: Api.Response.UserRead = useAppSelector((state: any) => state.user.data)
	const dispatch = useDispatch();
	const location = useLocation();
	const nav = useNavigate()
	const user_menu = [{
		to: '/info_system', content: 'Информационные системы', disabled: false
	}]

	const admin_menu = [...user_menu, {
		to: '/user', content: 'Пользователи', disabled: false
	}, {
		to: '/question', content: 'Опросник', disabled: false
	},
	{
		to: '/source', content: 'Источники', disabled: false
	},
	]

	const getNavLinks = () => {
		return user && user.is_superuser ? admin_menu : user_menu
	};

	const checkMe = async () => {
		const { data, isError } = await fetchGetUserMe()
		if (isError) {
			console.error('Me error');
			nav('/login?callback_url=' + location.pathname)
			return;
		}
		dispatch(setUser(data));
	}

	useEffect(() => {
		if (location.pathname === '/') {
			nav('/info_system')
		}
		console.log(user)
	}, [user])

	useEffect(() => {
		checkMe();
	}, []);

	const onLogout = () => {
		localStorage.removeItem('accessToken')
		nav('/login?callback_url=' + location.pathname)
	}

	const handleMenuClick = (v: any) => {
		console.log(v.key);

		nav(v.key)
	}

	return (
		<Layout style={{ height: '100%' }}>
			<Header style={{ margin: '2' }}>
				<Flex justify='space-between' style={{ height: '100%', alignItems: 'center' }} gap={16}>
					<Link to='/' style={{ height: '100%' }}>
						<Flex gap={16} align='center'>
							<img src={logo} alt='' height='48px' /><div className='logo_caption'>ФОРПОСТ</div>
						</Flex>
					</Link>
					{user && <>
						<Menu
							defaultSelectedKeys={['1']}
							defaultOpenKeys={['sub1']}
							mode='horizontal'
							disabledOverflow={true}
							onClick={(item: any) => handleMenuClick(item)}
							items={getNavLinks().map((link) => ({
								key: link.to,
								label: <a href={link.to}>{link.content}</a>,
							}))}
						>
						</Menu>
						<Flex gap={16} align='center'>
							<Typography.Text style={{ color: "white" }}>{user.email}</Typography.Text>
							<Button size='small' onClick={onLogout}>Выход</Button>
						</Flex>
					</>}
					{!user && <Button size='small' onClick={() => nav('/login?callback_url=' + location.pathname)}>Вход</Button>}
				</Flex>
			</Header>
			<Content style={{ margin: '24px 16px 0', overflow: 'auto' }}>
				<Flex>
					<Outlet />
				</Flex>
			</Content>
			<Footer >
				<Flex justify='center'>
					<Typography.Text style={{ color: '#FFFFFF' }}> Команда Ultra, 2024	</Typography.Text>
				</Flex>
			</Footer>
		</Layout >
	);
};

export default Main;
