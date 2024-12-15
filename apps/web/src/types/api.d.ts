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

        export interface UserRead {
            email: string;
            id: number;
            is_active: boolean;
            is_superuser: boolean;
            is_verified: boolean;
        }

        export interface UserReadList {
            email: string;
            id: number;
            is_active: boolean;
            is_superuser: boolean;
            is_verified: boolean;
        }

        export interface UserCreate {
            email: string;
            password: string;
            is_active?: boolean;
            is_superuser?: boolean;
            is_verified?: boolean;
        }


        export interface SystemRead {
            id: number
            create_at: string;
            name: string;
            description?: string
            repo?: string
            report: string
            chat?: object
            owner: UserRead
        }

        export interface SystemReadList {
            id: number
            create_at: string;
            name: string;
            repo?: string
            report: string
            owner: UserRead
        }

        export interface SystemCreate {
            name: string;
            owner: UserRead
        }

        export interface SourceRead {
            id: number
            name: string;
            url?: string
        }

        export interface SourceReadList {
            id: number
            name: string;
        }

        export interface SourceCreate {
            name: string;
        }

        export interface QuestionRead {
            id: number
            question: string;
            source?: SourceRead
        }

        export interface QuestionReadList {
            id: number
            question: string;
            answers?: AnswerRead[]
        }

        export interface QuestionCreate {
            question: string;
        }

        export interface AnswerRead {
            id: number
            answer: string;
            sec_value?: number
        }

        export interface AnswerReadList {
            id: number
            answer: string;
            sec_value?: number
        }

        export interface AnswerCreate {
            answer: string;
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
