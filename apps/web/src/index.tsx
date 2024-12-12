import ReactDOM from 'react-dom/client';

import { ConfigProvider } from 'antd';
import locale from 'antd/locale/ru_RU';
import { RouterProvider } from 'react-router-dom';
import './index.css';
import { Provider } from 'react-redux';
import { store } from './store';
import { router } from './router';
import theme from './theme.json';

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);

root.render(
	<ConfigProvider theme={theme} locale={locale}>
		<Provider store={store}>
			<RouterProvider router={router} future={{ v7_startTransition: true }} />
		</Provider>
	</ConfigProvider>
);
