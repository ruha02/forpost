import { Button, Form, message, Table, Typography } from "antd";
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
        console.log('selectedRowKeys changed: ', newSelectedRowKeys);
        setSelectedRowKeys(newSelectedRowKeys);
    };
    const onChange = (pagination: any, filters: any, sorter: any, extra: any) => {
        console.log('params', pagination, filters, sorter, extra);
    };
    const handelAdd = () => {
        setModalProps({
            isEdit: false,
            open: true,
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
                console.log('handle cancel');
                setModalProps((prev: any) => ({ ...prev, open: false }))

            },
            form: form
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
        const params = {
            offset: (page - 1) * pageSize,
            limit: pageSize
        };
        getList(params).then((data) => data && setList(data));
    }, [page, pageSize, total]);

    useEffect(() => {
        props.action.count().then((result) => {
            if (result.isError) {
                return;
            }
            setTotal(result.data);
        });
    }, [list]);



    return <>{contextHolder}<div style={{ display: 'flex', flexDirection: 'column', width: '100%', height: '100%' }}>
        <Typography.Title level={3} style={{ alignSelf: 'center' }}>{props.title}</Typography.Title>
        <div style={{ display: "flex", justifyContent: 'space-between', marginBottom: "16px" }}>
            <div>{hasSelected ? `Выбрано: ${selectedRowKeys.length}` : ''}</div>
            <div style={{ display: "flex", gap: "8px" }}>
                <Button type="primary" onClick={handelAdd}>Добавить</Button>
                <Button type="primary" danger={true} onClick={() => handelDelete(selectedRowKeys)} disabled={!hasSelected}>Удалить</Button>
                {props.buttons?.map((button, key) => (
                    <Button key={key} type={button.type} danger={button.danger} onClick={() => {
                        return button.onClick ? button.onClick() : button.onClickWithSelectedRow ? button.onClickWithSelectedRow(selectedRowKeys) : console.log(`Button ${button.title} have no action`);
                    }} disabled={button.onClick ? false : !hasSelected}>{button.title}</Button>
                ))}
            </div>
        </div>

        <Table
            loading={loading}
            style={{ cursor: 'pointer' }}
            dataSource={list}
            columns={props.fieldList}
            pagination={{
                defaultCurrent: 1,
                total: total,
                pageSize: pageSize,
                onChange: (page, pageSize) => { setPage(page); setPageSize(pageSize) },
                current: page,
            }}
            rowKey='id'
            onChange={onChange}
            rowSelection={rowSelection}
            onRow={(record, rowIndex) => {
                return {
                    onClick: async event => {
                        await getData(record['id'])
                        // setModalProps({
                        //     isEdit: true,
                        //     open: true,
                        //     onOk: (values: any) => {
                        //         props.action.add(values).then((res: any) => {
                        //             if (res.isError) {
                        //                 message.error('Ошибка создания')
                        //                 return
                        //             }
                        //             message.success('Успешно создано')
                        //             setModalProps((prev: any) => ({ ...prev, open: false }))
                        //             setTotal((prev) => prev + 1)
                        //         })
                        //     },
                        //     onCancel: () => {
                        //         setModalProps((prev: any) => ({ ...prev, open: false }))

                        //     },
                        //     form: form,
                        //     data: data
                        // })
                    }
                };
            }} />
        {props.modal(modalProps)}
    </div>
    </>
}

export default TableData