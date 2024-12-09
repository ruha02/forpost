import { fetchHandler, createQueryParamsString } from ".";


export async function getAnswers (params: Api.Params) {
    return await fetchHandler<Api.Response.AnswerReadList[]>('answer/' + createQueryParamsString(params));
}

export async function getAnswer (id: number) {
    return await fetchHandler<Api.Response.AnswerRead>('answer/' + id);
}

export async function updateAnswer(id: number, data: any) {

    return await fetchHandler<Api.Response.AnswerRead>('answer/' + id, {
        method: 'PATCH',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
        },
    });
}

export async function createAnswer(data: any) {
    return await fetchHandler<Api.Response.AnswerRead>('answer/', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
        },
    });
}

export async function deleteAnswer(id: number) {
    return await fetchHandler<Api.Response.Success>('answer/' + id, {
        method: 'DELETE',
    });
}

export async function countAnswers() {
    return await fetchHandler<number>('answer/count/');
}