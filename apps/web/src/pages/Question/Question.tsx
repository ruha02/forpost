
import { Form, Input, Modal } from 'antd';
import { TableData } from '../../components/TableData';
import { countQuestions, createQuestion, deleteQuestion, getQuestion, getQuestions, updateQuestion } from './../../api/question';

const Question: React.FC = () => {
    const getColorByGrade = (grade: number): string => {
        const colors = {
            1: '#0000ff',
            2: '#00ff00',
            3: '#ffff00',
            4: '#ff7f00',
            5: '#ff0000'
        }
        return colors[grade as keyof typeof colors] || '#ff0000'
    }
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
            render: (value: string) => value
        },
        {
            title: 'Источник',
            dataIndex: 'source',
            key: 'source',
            render: (value: Api.Response.SourceRead) => value ? <a href={value.url}>{value.name}</a> : '',
        },
        {
            title: 'Ответы',
            dataIndex: 'answers',
            key: 'answers',
            render: (value: Api.Response.AnswerReadList[]) => value ? value.map((answer: any) => <div style={{ color: getColorByGrade(answer.sec_value) }}> {answer.answer}</div >) : '',
        }
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
                <Form.Item label='Вопрос' name="question" key="question">
                    <Input />
                </Form.Item>
            </Form>
        </Modal>
    }

    return <TableData
        title='Вопросы'
        fieldList={FieldList}
        action={action}
        modal={get_modal}
    />
}
export default Question