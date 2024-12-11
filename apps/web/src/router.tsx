import { Navigate, createBrowserRouter } from 'react-router-dom';
import Main from './Main';

// import { Systems,  System, SystemEdit } from './pages/System';

// import { Users,  User, UserEdit } from './pages/User';

// import { Sources,  Source, SourceEdit } from './pages/Source';

// import { Questions,  Question, QuestionEdit } from './pages/Question';

// import { Answers,  Answer, AnswerEdit } from './pages/Answer';


export const router = createBrowserRouter([
	{
		path: '/',
		element: <Main />,
		// children: [

		// 	{
		// 		path: '/system',
		// 		element: (
		// 			<SystemList />
		// 		),
		// 	},
		// 	{
		// 		path: '/system/:id',
		// 		element: (
		// 			<System />
		// 		),
		// 	},
		// 	{
		// 		path: '/system/:id/edit',
		// 		element: (
		// 			<SystemEdit />
		// 		),
		// 	},

		// 	{
		// 		path: '/user',
		// 		element: (
		// 			<UserList />
		// 		),
		// 	},
		// 	{
		// 		path: '/user/:id',
		// 		element: (
		// 			<User />
		// 		),
		// 	},
		// 	{
		// 		path: '/user/:id/edit',
		// 		element: (
		// 			<UserEdit />
		// 		),
		// 	},

		// 	{
		// 		path: '/source',
		// 		element: (
		// 			<SourceList />
		// 		),
		// 	},
		// 	{
		// 		path: '/source/:id',
		// 		element: (
		// 			<Source />
		// 		),
		// 	},
		// 	{
		// 		path: '/source/:id/edit',
		// 		element: (
		// 			<SourceEdit />
		// 		),
		// 	},

		// 	{
		// 		path: '/question',
		// 		element: (
		// 			<QuestionList />
		// 		),
		// 	},
		// 	{
		// 		path: '/question/:id',
		// 		element: (
		// 			<Question />
		// 		),
		// 	},
		// 	{
		// 		path: '/question/:id/edit',
		// 		element: (
		// 			<QuestionEdit />
		// 		),
		// 	},

		// 	{
		// 		path: '/answer',
		// 		element: (
		// 			<AnswerList />
		// 		),
		// 	},
		// 	{
		// 		path: '/answer/:id',
		// 		element: (
		// 			<Answer />
		// 		),
		// 	},
		// 	{
		// 		path: '/answer/:id/edit',
		// 		element: (
		// 			<AnswerEdit />
		// 		),
		// 	},

		// ],
	},
	{
		path: '/login',
		element: <Login />,
	},
	{
		path: '*',
		element: <Navigate to='/' />,
	},
]);