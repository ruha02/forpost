import { BaseButtonProps } from "antd/es/button/button";

declare global {
    namespace Table {
        export interface FieldList {
            title: string;
            dataIndex: string;
            key: string;
            render?: (value: any) => JSX.Element | string;
        }

        export interface Field {
            title: string;
            render?: (value: any) => JSX.Element;
        }

        export interface Action {
            add: (data: any) => any;
            delete: (id: number) => Promise<Response<Success>>;
            update: (id: number, data: any) => any;
            get: (id: number) => any;
            count: () => Promise<Response<number>>;
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
            field: Field[];
            action: Action;
            buttons?: Button[];
            modal?: JSX.Element
        }

    }
} 