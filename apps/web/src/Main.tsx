import { Button, Flex, Menu, Layout, Typography, Tooltip } from 'antd';
import React from 'react';
import { Link, Outlet, useNavigate, useLocation } from 'react-router-dom';
import logo from './assets/logo_white.png';
import { useAppSelector } from './hooks/useAppSelector'
import { useEffect, useState } from 'react'
const { Content, Footer, Header } = Layout;




const Main: React.FC = () => {
	const user: Api.Response.UserRead = useAppSelector((state: any) => state.user.data)
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

	useEffect(() => {
		if (!user) {
			nav('/login?callback_url=' + location.pathname)
		}
		if (location.pathname === '/') {
			nav('/info_system')
		}
		console.log(user)
	}, [user])

	const onLogout = () => {
		localStorage.removeItem('accessToken')
		nav('/login?callback_url=' + location.pathname)
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

					<Menu
						defaultSelectedKeys={['1']}
						defaultOpenKeys={['sub1']}
						mode='horizontal'
						disabledOverflow={true}
					>
						{getNavLinks().map((link) => (
							<Menu.Item key={link.to} disabled={link.disabled}>
								<Tooltip title={link.content} mouseEnterDelay={0.75} color='#000000c1'>
									<Link
										to={link.to}
										key={link.to}
									>
										{link.content}
									</Link>
								</Tooltip>
							</Menu.Item>
						))}
					</Menu>
					<Flex gap={16} align='center'>
						<Typography.Text style={{ color: "white" }}>{user && user.email}</Typography.Text>
						<Button size='small' onClick={onLogout}>Выход</Button>
					</Flex>
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
		</Layout>
	);
};

export default Main;
