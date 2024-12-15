
import { CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons';
import { Flex, Form, Input, message, Modal, Switch } from 'antd';
import { TableData } from '../../components/TableData';
import { countUsers, createUser, deleteUser, getUser, getUsers, updateUser } from './../../api/user';
const User: React.FC = () => {
    const FieldList: Table.FieldList[] = [
        {
            title: 'ID',
            dataIndex: 'id',
            key: 'id',
            render: (value: string) => value
        },
        {
            title: 'Электронная почта',
            dataIndex: 'email',
            key: 'email',
            render: (value: string) => <a href={`mailto:${value}`} > {value}</a >,
        },
        {
            title: 'Активен',
            dataIndex: 'is_active',
            key: 'is_active',
            render: (value: boolean) => value ? <Flex justify="center"><CheckCircleOutlined style={{ fontSize: "1.1rem", color: "#00FF00" }} /></Flex> : <Flex justify="center"><CloseCircleOutlined style={{ fontSize: "1.1rem", color: "#FF0000" }} /></Flex>,
        },
        {
            title: 'Администратор',
            dataIndex: 'is_superuser',
            key: 'is_superuser',
            render: (value: boolean) => value ? <Flex justify="center"><CheckCircleOutlined style={{ fontSize: "1.1rem", color: "#00FF00" }} /></Flex> : <Flex justify="center"><CloseCircleOutlined style={{ fontSize: "1.1rem", color: "#FF0000" }} /></Flex>,
        }
    ]


    const action: Table.Action = {
        "add": createUser,
        "delete": deleteUser,
        "update": updateUser,
        "get": getUser,
        "count": countUsers,
        "get_list": getUsers
    }

    const buttons: Table.Button[] = [
        {
            title: 'Заблокировать',
            onClickWithSelectedRow: async (ids: Array<any>) => {
                ids.map(async (id) => {
                    const result = await updateUser(id, { is_active: false })
                    if (result.isError) {
                        message.error('Ошибка удаления')
                    }
                })
            },
        },
        {
            title: 'Разблокировать',
            onClickWithSelectedRow: (ids: Array<any>) => {
                ids.map(async (id) => {
                    const result = await updateUser(id, { is_active: true })
                    if (result.isError) {
                        message.error('Ошибка блокировки')
                    }
                })
            }
        }
    ]

    const get_modal = ({ isEdit, open, onOk, onCancel, data, form }: Table.ModalW) => {

        return <Modal
            title={isEdit ? "Редактирование" : "Добавление"}
            open={open}
            onOk={(values) => {
                form.validateFields().then((values: any) => {
                    onOk(values)
                }).catch((error: any) => {
                })
            }}
            onCancel={() => onCancel()}
            width={1000}
            height={800}
            closable={false}
        >
            <Form
                form={form}
                initialValues={undefined}
                labelCol={{ span: 6 }}
                wrapperCol={{ span: 16 }}>
                <Form.Item label="Электронная почта" name="email" key="email">
                    <Input />
                </Form.Item>
                {!data && <Form.Item label="Пароль" name="password" key="password">
                    <Input.Password />
                </Form.Item>}

                <Form.Item label='Активен' name="is_active" key="is_active" >
                    <Switch />
                </Form.Item>
                <Form.Item label='Администратор' name="is_superuser" key="is_superuser" >
                    <Switch />
                </Form.Item>
            </Form>
        </Modal>
    }

    return <TableData
        title='Информационные системы'
        fieldList={FieldList}
        buttons={buttons}
        action={action}
        modal={get_modal}
    />
}
export default User