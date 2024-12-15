import { createQueryParamsString, fetchHandler } from ".";


export async function getQuestions(params: Api.Params) {
    return await fetchHandler<Api.Response.QuestionReadList[]>('question/' + createQueryParamsString(params));
}

export async function getQuestion(id: number) {
    return await fetchHandler<Api.Response.QuestionRead>('question/' + id);
}

export async function updateQuestion(id: number, data: any) {
    data['source_id'] = Number(data['source']['id']);
    data['answers'].map((answer: any) => {
        answer['sec_value'] = answer['sec_value'] ? answer['sec_value'] : 3;
    });
    console.log(JSON.stringify(data));
    return await fetchHandler<Api.Response.QuestionRead>('question/' + id, {
        method: 'PATCH',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
        },
    });
}

export async function createQuestion(data: any) {
    data['source_id'] = Number(data['source']['id']);
    data['answers'].map((answer: any) => {
        answer['sec_value'] = answer['sec_value'] ? answer['sec_value'] : 3;
    });
    return await fetchHandler<Api.Response.QuestionRead>('question/', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
        },
    });
}

export async function deleteQuestion(id: number) {
    return await fetchHandler<Api.Response.Success>('question/' + id, {
        method: 'DELETE',
    });
}

export async function countQuestions(params?: Api.Params) {
    return await fetchHandler<number>('question/count/' + createQueryParamsString(params ? params : {}));
}