type ISOString = string;

declare namespace Api {
    export interface StringValidator {
        isAcceptable(s: string): boolean;
    }

    type Response<T> = { isError: false; data: T } | { isError: true; data: Api.Response.Error | null };

    type Params = { [key: string]: any };

    namespace Params {
        type Pagination = {
            offset?: number;
            limit?: number;
        };
        type PaginationWithSearch = {
            offset?: number;
            limit?: number;
            search_text?: string;
        };
    }

    namespace Response {
        export interface Error {
            detail: [
                {
                    loc: [string, number];
                    msg: string;
                    type: string;
                },
            ] | {
                diff?: number;
                message?: string;
            };
        }

        export interface Success {
            result: boolean;
        }

        export interface User {
            email: string;
            id: number;
            is_active: boolean;
            is_superuser: boolean;
            is_verified: boolean;
        }
        export type Users = Array<User>;


        export type Login = {
            access_token: string;
            token_type: string;
        };

    }

    namespace Request {

        export type Login = {
            username: string;
            password: string;
        };

    }
}
