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

export interface FeedEntry {
    id: string;
    created: number;
}

export interface FeedResponse {
    feed: FeedEntry[];
}

export async function queryFeed(groupId: string): Promise<FeedResponse> {
    return await http<FeedResponse>({
        url: "/v1/graphql",
        headers: getAuthHeaders(),
        method: "POST",
        data: {
            query: "{ myself { id name email picture } groups { id } }",
        },
    });
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
    return await http<GroupsResponse>({
        url: "/v1/graphql",
        headers: getAuthHeaders(),
        method: "POST",
        data: {
            query: "{ myself { id name email picture } groups { id } }",
        },
    });
}
