
import { Button, Card, Divider, Flex, Form, Input, Modal, Radio, Select } from 'antd';
import { useEffect, useState } from 'react';
import { getSources } from '../../api/source';
import { TableData } from '../../components/TableData';
import { countQuestions, createQuestion, deleteQuestion, getQuestion, getQuestions, updateQuestion } from './../../api/question';
const Question: React.FC = () => {
    const [sources, setSources] = useState<Api.Response.SourceReadList[]>([])

    const getSourcesFilter = async () => {
        const { data, isError } = await getSources({ offset: 0 });
        if (isError) {
            return;
        }
        setSources(data);
    }

    useEffect(() => {
        getSourcesFilter()
    }, [])

    const FieldList: Table.FieldList[] = [
        {
            title: 'ID',
            dataIndex: 'id',
            key: 'id',
            render: (value: string) => value
        },
        {
            title: 'Вопрос',
            dataIndex: 'question',
            key: 'question',
            render: (value: string) => value,
        },
        {
            title: 'Источник',
            dataIndex: 'source',
            key: 'source_id',
            render: (value: Api.Response.SourceRead) => value ? <a href={value.url}>{value.name}</a> : '',
            filters: sources && sources.map((source: Api.Response.SourceReadList) => ({ text: source.name, value: source.id })),
            onFilter: (value: number, record: Api.Response.QuestionRead) => {
                return record.source?.id === value
            },
            filterSearch: true,
            filterMultiple: false,
            onChange: (value: number) => {
                console.log(value);
            }
        },
    ]


    const action: Table.Action = {
        "add": createQuestion,
        "delete": deleteQuestion,
        "update": updateQuestion,
        "get": getQuestion,
        "count": countQuestions,
        "get_list": getQuestions
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
                <Form.Item label='Вопрос' name="question" key="question">
                    <Input />
                </Form.Item>
                <Form.Item label='Источник' name={["source", "id"]} key="source_id">
                    <Select
                        showSearch
                        filterOption={(input, option) =>
                            (option?.label ?? '').toLowerCase().includes(input.toLowerCase())
                        }
                        options={sources.map((source: Api.Response.SourceReadList) => ({ label: source.name, value: source.id }))}
                    />
                </Form.Item>
                <Divider>Ответы</Divider>

                <Form.List name="answers" >
                    {(fields, { add, remove }) => (
                        <>
                            {fields.map(({ key, name, ...restField }) => (
                                <Card
                                    title={`Ответ ${key + 1}`}
                                    size='small'
                                    extra={
                                        <Button
                                            type="primary"
                                            size='small'
                                            danger
                                            onClick={() => remove(name)}
                                        >
                                            Удалить
                                        </Button>}
                                    style={{ width: "100%", marginBottom: '24px' }}>
                                    <Form.Item key={key}>
                                        <Flex vertical >
                                            <Form.Item label='Значение' {...restField} name={[name, 'answer']} style={{ width: "100%" }}>
                                                <Input />
                                            </Form.Item>
                                            <Form.Item label='Уровень опасности' {...restField} name={[name, 'sec_value']} key={`sec_value_${key}`}>
                                                <Radio.Group
                                                    block
                                                    options={[
                                                        { label: 'Не несёт', value: 1, style: { width: "120px" } },
                                                        { label: 'Низкий', value: 2, style: { width: "120px" } },
                                                        { label: 'Средний', value: 3, style: { width: "120px" } },
                                                        { label: 'Высокий', value: 4, style: { width: "120px" } },
                                                        { label: 'Критичный', value: 5, style: { width: "120px" } },
                                                    ]}
                                                    defaultValue={3}
                                                    optionType="button"
                                                    buttonStyle="solid"
                                                />
                                            </Form.Item>
                                        </Flex>
                                    </Form.Item>
                                </Card>
                            ))}
                            <Form.Item>
                                <Button type="primary" onClick={() => add()}>Добавить ответ</Button>
                            </Form.Item>
                        </>
                    )}
                </Form.List>





                {/* <Form.List name="answers">
                    {(fields, { add, remove }) => (
                        <>
                            {fields.map(({ key, name, ...restField }) => (
                               
                                    
                                </Card>
                            ))}
                            <Button type="primary" onClick={() => add() > Добавить ответ</Button>
                    )}
                </Form.List> */}
            </Form >
        </Modal >
    }

    return <TableData
        title='Вопросы'
        fieldList={FieldList}
        action={action}
        modal={get_modal}
    />
}
export default Question