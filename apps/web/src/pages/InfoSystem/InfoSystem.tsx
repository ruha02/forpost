
import { Form, Input, message, Modal } from 'antd';
import { TableData } from '../../components/TableData';
import { countSystems, createSystem, deleteSystem, getSystem, getSystems, updateSystem } from './../../api/system';

const System: React.FC = () => {


    const FieldList: Table.FieldList[] = [
        {
            title: 'ID',
            dataIndex: 'id',
            key: 'id',
            render: (value: string) => value
        },
        {
            title: 'Дата создания',
            dataIndex: 'create_at',
            key: 'create_at',
            render: (value: string) => {
                const d = new Date(value)
                return `${d.getDate()}.${d.getMonth()}.${d.getFullYear()}`
            }
        },
        {
            title: 'Наименование',
            dataIndex: 'name',
            key: 'name',
            render: (value: string) => <>{value}</>,
        },
        {
            title: 'Репозиторий',
            dataIndex: 'repo',
            key: 'repo',
            render: (value: string) => <a href={value} target='_blank' rel='noreferrer'><>{value}</></a>,
        },
        {
            title: 'Отчет',
            dataIndex: 'report',
            key: 'report',
            render: (value: string) => value === null ? "Отсутствует" : <a href={value} target='_blank' rel='noreferrer'>Скачать{value}</a>,
        },
        {
            title: 'Автор',
            dataIndex: 'owner',
            key: 'owner',
            render: (value: Api.Response.UserRead) => <a href={`mailto:${value.email}`} > {value.email}</a >,
        },

    ]


    const action: Table.Action = {
        "add": createSystem,
        "delete": deleteSystem,
        "update": updateSystem,
        "get": getSystem,
        "count": countSystems,
        "get_list": getSystems
    }

    const buttons: Table.Button[] = [
        {
            title: 'Заблокировать',
            onClickWithSelectedRow: async (ids: Array<any>) => {
                ids.map(async (id) => {
                    const result = await deleteSystem(id)
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
                    const result = await updateSystem(id, { is_active: true })
                    if (result.isError) {
                        message.error('Ошибка блокировки')
                    }
                })
            }
        }
    ]

    const get_modal = ({ isEdit, open, onOk, onCancel, data, form }: Table.ModalW) => {
        console.log(data);

        return <Modal
            title={isEdit ? "Редактирование" : "Добавление"}
            open={open}
            onOk={(values) => {
                form.validateFields().then((values: any) => {
                    onOk(JSON.stringify(values))
                }).catch((error: any) => {
                    console.log(error);
                })
            }}
            onCancel={() => onCancel()}
            width={1000}
            height={800}
            closable={false}
        >
            <Form
                form={form}
                initialValues={isEdit ? { ...data } : undefined}
                labelCol={{ span: 6 }}
                wrapperCol={{ span: 16 }}>
                <Form.Item label='Наименование' name="name" key="name">
                    <Input />
                </Form.Item>
                <Form.Item label='Описание' name="description" key="description">
                    <Input.TextArea />
                </Form.Item>
                <Form.Item label='Ссылка на репозиторий' name="repo" key="repo">
                    <Input />
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
};
export default System