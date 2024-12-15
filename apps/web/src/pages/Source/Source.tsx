
import { Form, Input, Modal } from 'antd';
import { TableData } from '../../components/TableData';
import { countSources, createSource, deleteSource, getSource, getSources, updateSource } from './../../api/source';

const Source: React.FC = () => {
    const FieldList: Table.FieldList[] = [
        {
            title: 'ID',
            dataIndex: 'id',
            key: 'id',
            render: (value: string) => value
        },
        {
            title: 'Наименование',
            dataIndex: 'name',
            key: 'name',
            render: (value: string) => value
        },
        {
            title: 'Ссылка',
            dataIndex: 'url',
            key: 'url',
            render: (value: string) => value ? <a href={value} target='_blank'>{value}</a> : '',
        },
    ]


    const action: Table.Action = {
        "add": createSource,
        "delete": deleteSource,
        "update": updateSource,
        "get": getSource,
        "count": countSources,
        "get_list": getSources
    }

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
                <Form.Item label='Наименование' name="name" key="name">
                    <Input />
                </Form.Item>
                <Form.Item label='Ссылка' name="url" key="url">
                    <Input addonBefore="https://" />
                </Form.Item>
            </Form>
        </Modal>
    }

    return <TableData
        title='Источники вопросов'
        fieldList={FieldList}
        action={action}
        modal={get_modal}
    />
}
export default Source