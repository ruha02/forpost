import { EditOutlined } from "@ant-design/icons";
import { Button, Flex, Form, message, Popconfirm, Table, Typography } from "antd";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";



const TableData = (props: Table.Props) => {
    const navigate = useNavigate()
    const [messageApi, contextHolder] = message.useMessage({ duration: 5 });
    const [form] = Form.useForm();
    // states
    const [loading, setLoading] = useState(false);
    const [list, setList] = useState([])
    const [data, setData] = useState<any>({});
    const [page, setPage] = useState(1)
    const [pageSize, setPageSize] = useState(10)
    const [total, setTotal] = useState(10)
    const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([]);
    const [modalProps, setModalProps] = useState<Table.ModalW>({
        isEdit: false,
        open: false,
        onOk: () => { },
        onCancel: () => { },
        data: [],
        form: form,
    });
    const [params, setParams] = useState({
        offset: 0,
        limit: 10,
    })

    // get data
    const getList = async (params: Api.Params.Pagination) => {
        setLoading(true);
        const result = await props.action.get_list(params);
        if (result.isError) {
            messageApi.error('Ошибка при получении данных');
            setLoading(false);
            return;
        }
        setLoading(false);
        return result.data;
    }

    const getData = async (id: number) => {
        setLoading(true);
        const result = await props.action.get(id);
        if (result.isError) {
            messageApi.error('Ошибка при получении данных');
            setLoading(false);
            return;
        }
        setLoading(false);
        setData(result.data);
        return result.data;
    }

    // handlers
    const onSelectChange = (newSelectedRowKeys: React.Key[]) => {
        setSelectedRowKeys(newSelectedRowKeys);
    };

    const handelAdd = () => {
        form.resetFields();
        setModalProps({
            isEdit: false,
            open: true,
            data: null,
            onOk: (values: any) => {
                console.log(values);

                props.action.add(values).then((res: any) => {
                    if (res.isError) {
                        message.error('Ошибка создания')
                        return
                    }
                    message.success('Успешно создано')
                    setModalProps((prev: any) => ({ ...prev, open: false }))
                    setTotal((prev) => prev + 1)
                })
            },
            onCancel: () => {
                setModalProps((prev: any) => ({ ...prev, open: false }))

            },
            form: form
        })
    }

    const handelEdit = (id: number) => {
        getData(id).then((data) => {
            console.log(data);

            form.setFieldsValue(data)
            setModalProps({
                isEdit: true,
                open: true,
                data: data,
                onOk: (values: any) => {
                    console.log(values);
                    props.action.update(id, values).then((res: any) => {
                        if (res.isError) {
                            message.error('Ошибка создания')
                            return
                        }
                        message.success('Успешно создано')
                        setModalProps((prev: any) => ({ ...prev, open: false }))
                        setTotal((prev) => prev + 1)
                    })
                },
                onCancel: () => {
                    setModalProps((prev: any) => ({ ...prev, open: false }))

                },
                form: form
            })
        })
    }

    const handelDelete = async (ids: Array<any>) => {
        ids.map(async (id) => {
            const result = await props.action.delete(id)
            if (result.isError) {
                message.error('Ошибка удаления')
            }
            setTotal((prev) => prev - 1)
        })
    }

    // another constants
    const rowSelection = {
        selectedRowKeys,
        onChange: onSelectChange,
    };
    const hasSelected = selectedRowKeys.length > 0;


    // effects
    useEffect(() => {
        getList(params).then((data) => data && setList(data));
    }, [params, total]);

    useEffect(() => {
        props.action.count(params).then((result) => {
            if (result.isError) {
                return;
            }
            setTotal(result.data);
        });

    }, [list, params]);

    const onChange = (pagination: any, filters: any, extras: any) => {
        let params = {
            offset: (pagination['current'] - 1) * pagination['pageSize'],
            limit: pageSize,
        };
        for (const key in filters) {
            if (filters[key]) {
                params = {
                    ...params,
                    [key]: filters[key][0]
                }
            }
        }
        setParams(params);
    };

    return <>{contextHolder}<div style={{ display: 'flex', flexDirection: 'column', width: '100%', height: '100%' }}>
        <Typography.Title level={3} style={{ alignSelf: 'center' }}>{props.title}</Typography.Title>
        <div style={{ display: "flex", justifyContent: 'space-between', marginBottom: "16px" }}>
            <div>{hasSelected ? `Выбрано: ${selectedRowKeys.length}` : ''}</div>
            <div style={{ display: "flex", gap: "8px" }}>
                <Button type="primary" onClick={handelAdd}>Добавить</Button>
                <Popconfirm title={`Вы уверены что хотите удалить: ${selectedRowKeys.length} шт.?`} onConfirm={() => handelDelete(selectedRowKeys)} okText="Да" cancelText="Нет">
                    <Button type="primary" danger={true} disabled={!hasSelected}>Удалить</Button>
                </Popconfirm>
                {props.buttons?.map((button, key) => (
                    <Button key={key} type={button.type} danger={button.danger} onClick={() => {
                        return button.onClick ? button.onClick() : button.onClickWithSelectedRow ? button.onClickWithSelectedRow(selectedRowKeys) : console.log(`Button ${button.title} have no action`);
                    }} disabled={button.onClick ? false : !hasSelected}>{button.title}</Button>
                ))}
            </div>
        </div>

        <Table
            loading={loading}
            dataSource={list}
            onChange={onChange}
            columns={[...props.fieldList,
            {
                title: 'Действия',
                dataIndex: 'id',
                key: 'actions',
                render: (value: number) => <Flex justify="center">
                    <EditOutlined
                        style={{ fontSize: "1.1rem" }}
                        onClick={() => { return handelEdit(value) }} />
                </Flex>
            }
            ]}
            pagination={{
                defaultCurrent: 1,
                total: total,
                pageSize: pageSize,
                onChange: (page, pageSize) => { setPage(page); setPageSize(pageSize) },
                current: page,
            }}
            rowKey='id'
            rowSelection={rowSelection}
        />
        {props.modal(modalProps)}
    </div>
    </>
}

export default TableData