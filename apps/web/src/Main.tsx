import { Button, Flex, Input, Layout, Typography, Upload } from 'antd';
import type { UploadProps } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import React from 'react';
import { Link, Outlet } from 'react-router-dom';
import logo from './assets/logo.png';
import { API_URL } from './api';
import { UploadFile } from './components/UploadFile';
const { Content, Footer, Header } = Layout;
const { Search } = Input




const Main: React.FC = () => {
	const uploadProps: UploadProps = {
		name: 'file',
		action: `${API_URL}video`,
		onChange(info) {
			if (info.file.status !== 'uploading') {
				console.log(info.file, info.fileList);
			}
			if (info.file.status === 'done') {
				console.log(`${info.file.name} file uploaded successfully`);
			} else if (info.file.status === 'error') {
				console.error(`${info.file.name} file upload failed.`);
			}
		},
	};
	return (
		<Layout style={{ height: '100%' }}>
			<Header style={{ margin: '0' }}>
				<Flex style={{ height: '100%', alignItems: 'center' }} gap={16}>
					<Link to='/' style={{ height: '100%' }}><img src={logo} alt='' height='100%' /></Link>
					<Search placeholder='поиск по видео' />
					<UploadFile />
					<Link to='/video' ><Button>Мои видео</Button></Link>
				</Flex>
			</Header>
			<Content style={{ margin: '24px 16px 0', overflow: 'auto' }}>
				<Flex>
					<Outlet />
				</Flex>
			</Content>
			<Footer >
				<Flex justify='center'>
					<Typography.Text style={{ color: '#FFFFFF' }}> Команда Good Genius, 2024	</Typography.Text>
				</Flex>
			</Footer>
		</Layout>
	);
};

export default Main;
