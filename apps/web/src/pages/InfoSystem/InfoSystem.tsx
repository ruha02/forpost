
import { Button, Flex, Form, Input, Modal, Steps } from 'antd';
import ButtonGroup from 'antd/es/button/button-group';
import React, { useEffect, useRef, useState } from 'react';
import { Input as ChatInput, MessageBox } from 'react-chat-elements';
import 'react-chat-elements/dist/main.css';
import { TableData } from '../../components/TableData';
import { countSystems, createSystem, deleteSystem, getSystem, getSystemChat, getSystemReport, getSystems, sendSystemChatMessage, updateSystem } from './../../api/system';
// Required CSS for react-chat-elements
import 'react-chat-elements/dist/main.css';
import Markdown from 'react-markdown';

const Chat = ({ id }: { id: number }) => {
    const [messages, setMessages] = useState<any[]>([])
    const [message, setMessage] = useState('')
    const elementRef = useRef<HTMLDivElement>(null);
    const getChat = async () => {
        const result = await getSystemChat(id);
        if ((result.data) && (!result.isError)) {
            setMessages(result.data)
        }
    }

    const sendMessage = async (text: string) => {
        const result = await sendSystemChatMessage(id, text)
        if ((result.data) && (!result.isError)) {
            setMessages(result.data)
        }
    }

    const offset = (new Date()).getTimezoneOffset();

    useEffect(() => {
        if (messages.length === 0) {
            sendMessage("begin")
        }
        getChat()
    }, [id])

    return (
        <Flex vertical style={{ width: '100%' }}>
            <div style={{ height: '80%', border: '1px solid #ddd', overflowY: 'scroll', padding: '16px', marginBottom: '16px' }} ref={elementRef}>
                {messages.map((message, index) => (
                    <MessageBox
                        position={message.role === 'system' ? 'left' : 'right'}
                        type={'text'}
                        title={message.role === 'system' ? 'ФОРПОСТ' : 'Вы'}
                        text={message.text}
                        date={new Date((new Date(message.date)).getTime() - offset * 60000)}
                        id={index}
                        focus={false}
                        titleColor={'#4f81a1'}
                        forwarded={false}
                        replyButton={false}
                        removeButton={false}
                        status={'sent'}
                        notch={true}
                        retracted={false}
                    />
                ))}
            </div>
            <ChatInput
                placeholder="Введите сообщение"
                multiline={false}
                maxHeight={100}
                value={message}
                onChange={(e: any) => setMessage(e.target.value)}
                inputStyle={{ border: '1px solid #ddd' }}
                rightButtons={<Button type="primary" onClick={(e) => {
                    sendMessage(message)
                    if (elementRef.current) {
                        elementRef.current?.scrollIntoView({ behavior: 'smooth' });
                    }
                }}>Отправить</Button >}
                onSubmit={(e: any) => console.log(e.target.value)}
            />
        </Flex>
    )
}


const Report = ({ id }: { id: number }) => {
    const [report, setReport] = useState<any>()
    const [loading, setLoading] = useState(false)
    const getReport = async () => {
        setLoading(true)
        const result = await getSystemReport(id)
        if ((result.data) && (!result.isError)) {
            setReport(result.data)
        }
        setLoading(false)
    }

    useEffect(() => {
        getReport()
    }, [id])

    const handleUpdate = async () => {
        await getReport()
    }

    return <Flex vertical style={{ height: '90%', border: '1px solid #ddd', overflowY: 'scroll', padding: '16px', marginBottom: '16px', width: "900px" }}>
        {report ?
            <Markdown >
                {report}
            </Markdown>
            : <Button onClick={handleUpdate} loading={loading}>Запросить отчет</Button>}
    </Flex>
}

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

    const get_modal = ({ isEdit, open, onOk, onCancel, data, form }: Table.ModalW) => {
        const steps = [
            <Form
                form={form}
                initialValues={undefined}
                labelCol={{ span: 6 }}
                wrapperCol={{ span: 16 }}
                style={{ width: '100%', height: '600px' }}>
                <Form.Item label='Наименование' name="name" key="name">
                    <Input />
                </Form.Item>
                <Form.Item label='Описание' name="description" key="description">
                    <Input.TextArea />
                </Form.Item>
                <Form.Item label='Ссылка на репозиторий' name="repo" key="repo">
                    <Input />
                </Form.Item>
            </Form >,
            <Chat id={data && data.id ? data.id : 0} />,
            <Flex align='center' justify='center' style={{ height: '100%' }}>
                <Report id={data && data.id ? data.id : 0} />
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
            <Flex justify='center' style={{ height: '600px', width: '100%' }}>
                {steps[current]}
            </Flex>
            <Flex justify='space-between'>
                <ButtonGroup>
                    {current > 0 && <Button onClick={() => setCurrent(current - 1)}>
                        Назад
                    </Button>}
                    {current < steps.length - 1 && <Button onClick={() => setCurrent(current + 1)}>
                        Далее
                    </Button>}
                </ButtonGroup>
                <Button type="primary" onClick={(values) => {
                    form.validateFields().then((values: any) => {
                        onOk(values)
                    }).catch((error: any) => {
                    })
                }}>
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