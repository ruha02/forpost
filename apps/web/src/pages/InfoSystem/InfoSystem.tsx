
import { useState } from 'react'
import { message } from 'antd';
import { getSystems, getSystem, countSystems, deleteSystem, updateSystem, createSystem } from './../../api/system'
import { TableData } from '../../components/TableData';

const System: React.FC = () => {
    const [add, setAdd] = useState(false)
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

    const Field: Table.Field[] = [...(FieldList.map((field) => ({
        title: field.title,
        render: (value: string) => <>{value}</>,
    }))),
    {
        title: 'Описание',
        render: (value: string) => <>{value}</>,

    }]

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



    return <TableData
        title='Информационные системы'
        field={Field}
        fieldList={FieldList}
        buttons={buttons}
        action={action}
    />
};
export default System