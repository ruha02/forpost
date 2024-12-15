import { BaseButtonProps } from "antd/es/button/button";

declare global {

    namespace Table {
        export interface ModalW {
            isEdit: boolean;
            open: boolean;
            onOk: (values: any) => void;
            onCancel: () => void;
            data?: any;
            form: any;
        }

        export interface FieldList {
            title: string;
            dataIndex: string;
            key: string;
            render?: (value: any) => JSX.Element | string | any;
            filters?: any,
            onFilter?: (value: any, record: any) => boolean;
            onChange?: (value: any) => void;
            filterSearch?: boolean;
            filterMultiple?: boolean;
        }


        export interface Action {
            add: (data: any) => any;
            delete: (id: number) => Promise<Response<Success>>;
            update: (id: number, data: any) => any;
            get: (id: number) => any;
            count: (params: any) => Promise<Response<number>>;
            get_list: (params: Api.Params) => Promise<Response<any[]>>;
        }

        export interface Button {
            title: string;
            type?: BaseButtonProps['type'];
            danger?: boolean;
            onClick?: () => void;
            onClickWithSelectedRow?: (ids: React.Key[]) => void;
        }
        export interface Props {
            title: string;
            fieldList: FieldList[];
            action: Action;
            buttons?: Button[];
            modal: any;
        }

    }
} 