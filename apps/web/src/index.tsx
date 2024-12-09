import ReactDOM from 'react-dom/client';

import { ConfigProvider } from 'antd';
import locale from 'antd/locale/ru_RU';
import { RouterProvider } from 'react-router-dom';
import './index.css';
import { router } from './router.tsx';
import theme from './theme.json';

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);

root.render(
	<ConfigProvider theme={theme} locale={locale}>
		<RouterProvider router={router} />
	</ConfigProvider>
);
