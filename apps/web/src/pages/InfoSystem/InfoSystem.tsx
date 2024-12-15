
import { Button, Flex, Form, Input, Modal, Steps } from 'antd';
import ButtonGroup from 'antd/es/button/button-group';
import { useState } from 'react';
import { Input as ChatInput, MessageBox } from 'react-chat-elements';
import 'react-chat-elements/dist/main.css';
import { TableData } from '../../components/TableData';
import { countSystems, createSystem, deleteSystem, getSystem, getSystems, updateSystem } from './../../api/system';

const System: React.FC = () => {
    const [current, setCurrent] = useState(0)

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

    const handleSave = (values: any) => {
        console.log(values)
    }

    const get_modal = ({ isEdit, open, onOk, onCancel, data, form }: Table.ModalW) => {
        let currentIdMessage = data && data.chat ? data.chat.length : 0
        // setChat(data && data.chat ? data.chat : [])
        const createForpostMessage = (dateMessage: Date, textMessage: string) => {
            return <MessageBox
                position={'left'}
                type={'text'}
                title={'ФОРПОСТ'}
                text={textMessage}
                date={dateMessage}
                id={currentIdMessage}
                focus={false}
                titleColor={'#4f81a1'}
                forwarded={false}
                replyButton={false}
                removeButton={false}
                status={'sent'}
                notch={true}
                retracted={false}
            />
        }
        const createUserMessage = (dateMessage: Date, textMessage: string) => {
            return <MessageBox
                position={'right'}
                type={'text'}
                title={'Вы'}
                text={textMessage}
                date={dateMessage}
                id={currentIdMessage}
                focus={false}
                titleColor={'#4f81a1'}
                forwarded={false}
                replyButton={false}
                removeButton={false}
                status={'sent'}
                notch={true}
                retracted={false}
            />
        }
        const steps = [
            <>
                <Form.Item label='Наименование' name="name" key="name">
                    <Input />
                </Form.Item>
                <Form.Item label='Описание' name="description" key="description">
                    <Input.TextArea />
                </Form.Item>
                <Form.Item label='Ссылка на репозиторий' name="repo" key="repo">
                    <Input />
                </Form.Item>
            </ >,
            <>
                <div style={{ height: '80%', border: '1px solid #ddd', overflowY: 'scroll', padding: '10px', marginBottom: "10px" }}>
                    {createForpostMessage(new Date(), 'Привет. Я помощник для иследования твоей системы на вопросы информационной безопасности. Сейчас я изучаю твою систему и вскоре задам пару вопросов. Поджожди немного...')}
                </div>
                <ChatInput
                    placeholder="Введите сообщение"
                    multiline={false}
                    maxHeight={100}
                    rightButtons={<Button type="primary" onClick={() => {
                        console.log(form.getFieldsValue())
                        console.log(data)
                    }}>Отправить</Button >}
                    inputStyle={{ border: '1px solid #ddd' }
                    }
                    onSubmit={(e: any) => console.log(e.target.value)}
                />
            </>,
            <Flex align='center' justify='center' style={{ height: '100%' }}>
                <div>
                    {data.report ? <a href={data.report} target='_blank' rel='noreferrer'>Скачать отчет</a> : <>Очет формируется</>}
                </div>
            </Flex>
        ]


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
            closable={true}
            footer={null}
        >
            <Steps current={current} items={[
                {
                    title: 'Шаг 1',
                    description: 'Заполнение основных данных',
                },
                {
                    title: 'Шаг 2',
                    description: 'Опрос',
                },
                {
                    title: 'Шаг 3',
                    description: 'Получение отчета',
                }
            ]} />
            <Form
                form={form}
                initialValues={undefined}
                labelCol={{ span: 6 }}
                wrapperCol={{ span: 16 }}
                style={{ width: '100%', height: '600px' }}>
                {steps[current]}
            </Form>
            <Flex justify='space-between'>
                <ButtonGroup>
                    {current > 0 && <Button onClick={() => setCurrent(current - 1)}>
                        Назад
                    </Button>}
                    {current < steps.length - 1 && <Button onClick={() => setCurrent(current + 1)}>
                        Далее
                    </Button>}
                </ButtonGroup>
                <Button type="primary" onClick={() => console.log(form.getFieldsValue())}>
                    Сохранить
                </Button>
            </Flex>
        </Modal >
    }

    return <TableData
        title='Информационные системы'
        fieldList={FieldList}
        action={action}
        modal={get_modal}
    />
};
export default System