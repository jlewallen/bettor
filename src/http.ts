import { Config } from "@/config";

export function saveAuthHeaders(headers: Record<string, string>): void {
    window.localStorage["bettor:headers"] = JSON.stringify(headers);
}

export function getAuthHeaders(): Record<string, string> | undefined {
    const stored = window.localStorage["bettor:headers"];
    if (stored) {
        return JSON.parse(stored);
    }
    return undefined;
}

export function authenticated(): boolean {
    return window.localStorage["bettor:headers"] != null;
}

import { GraphQLClient } from "graphql-request";
import { getSdk } from "@/generated/graphql";

/*
import { ApolloClient, InMemoryCache, gql } from "@apollo/client/core";

const apollo = new ApolloClient({
    uri: "http://127.0.0.1:5000/v1/graphql",
    cache: new InMemoryCache(),
});
*/

export function getApi() {
    const gqlc = new GraphQLClient("http://127.0.0.1:5000/v1/graphql", {
        headers: getAuthHeaders(),
    });
    return getSdk(gqlc);
}

export interface OurRequestInfo {
    url: string;
    method?: string;
    data?: any;
    headers?: { [index: string]: string };
}

export async function http<T>(info: OurRequestInfo): Promise<T> {
    let body: string | null = null;
    if (info.data) {
        body = JSON.stringify(info.data);
    }
    const response = await fetch(Config.baseUrl + info.url, {
        method: info.method || "GET",
        mode: "cors",
        headers: Object.assign(
            {
                "Content-Type": "application/json",
            },
            info.headers
        ),
        body: body,
    });
    return await response.json();
}

export async function getLoginUrl(): Promise<string> {
    const response = await http<{ url: string }>({ url: "/v1/login" });
    return response.url;
}

export interface Person {
    sub: string;
    email: string;
    name: string;
    picture: string;
}

export interface LoginResponse {
    token: string;
    user: Person;
}

export async function login(code: string): Promise<LoginResponse> {
    const response = await http<LoginResponse>({
        url: "/v1/login",
        method: "POST",
        data: { code: code },
    });
    saveAuthHeaders({
        Authorization: `Bearer ${response.token}`,
    });
    return response;
}

export async function graphql<T>(query: string): Promise<T> {
    const res = await http<{ data: T }>({
        url: "/v1/graphql",
        headers: getAuthHeaders(),
        method: "POST",
        data: {
            query: query,
        },
    });
    return res.data;
}

export interface Group {
    id: string;
    name: string;
    members: Person[];
}

export interface GroupsResponse {
    groups: Group[];
}

export async function queryGroups(): Promise<GroupsResponse> {
    return await graphql<GroupsResponse>(`
        query {
            groups {
                id
                owner {
                    id
                    name
                    picture
                }
                name
                activityAt
                picture
                allBets {
                    id
                    title
                    details
                    createdAt
                    expiresAt
                    activityAt
                    state
                    author {
                        id
                        name
                        email
                    }
                    positions {
                        title
                        userPositions {
                            user {
                                id
                                name
                                email
                            }
                            createdAt
                            state
                        }
                    }
                }
            }
        }
    `);
}

export interface Bet {
    id: string;
    title: string;
    details: string;
    activityAt: string;
}

export interface ChatMessage {
    id: number;
    createdAt: string;
    message: string;
}

export interface ChatResponse {
    messages: ChatMessage[];
}

export async function groupChat(groupId: number, page: number): Promise<ChatResponse> {
    const response = await graphql<{ groupChat: ChatMessage[] }>(`
        query {
			groupChat(groupId: ${groupId}, page: ${page}) {
				id
				createdAt
				message
				author { id name picture }
			}
        }
	`);
    return { messages: response.groupChat };
}

export async function betChat(betId: number, page: number): Promise<ChatResponse> {
    const response = await graphql<{ betChat: ChatMessage[] }>(`
        query {
			betChat(betId: ${betId}, page: ${page}) {
				id
				createdAt
				message
				author { id name picture }
			}
        }
    `);
    return { messages: response.betChat };
}
