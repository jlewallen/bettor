import { GraphQLClient } from 'graphql-request';
import { print } from 'graphql';
import gql from 'graphql-tag';
export type Maybe<T> = T | null;
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]?: Maybe<T[SubKey]> };
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]: Maybe<T[SubKey]> };
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: string;
  String: string;
  Boolean: boolean;
  Int: number;
  Float: number;
  /**
   * The `DateTime` scalar type represents a DateTime
   * value as specified by
   * [iso8601](https://en.wikipedia.org/wiki/ISO_8601).
   */
  DateTime: any;
};

export type Query = {
  __typename?: 'Query';
  myself?: Maybe<User>;
  groups?: Maybe<Array<Maybe<Group>>>;
  bets?: Maybe<Array<Maybe<Bet>>>;
  groupChat?: Maybe<Array<Maybe<GroupChat>>>;
  betChat?: Maybe<Array<Maybe<BetChat>>>;
};


export type QueryGroupsArgs = {
  groupId?: Maybe<Scalars['Int']>;
};


export type QueryBetsArgs = {
  betId?: Maybe<Scalars['Int']>;
};


export type QueryGroupChatArgs = {
  groupId: Scalars['Int'];
  page: Scalars['Int'];
};


export type QueryBetChatArgs = {
  betId: Scalars['Int'];
  page: Scalars['Int'];
};

export type User = {
  __typename?: 'User';
  id: Scalars['ID'];
  sub: Scalars['String'];
  name: Scalars['String'];
  email: Scalars['String'];
  picture?: Maybe<Scalars['String']>;
  createdAt: Scalars['DateTime'];
  activityAt: Scalars['DateTime'];
  deletedAt?: Maybe<Scalars['DateTime']>;
  createdGroups?: Maybe<Array<Maybe<Group>>>;
  groups?: Maybe<Array<Maybe<Group>>>;
  authoredBets?: Maybe<Array<Maybe<Bet>>>;
  watchedBets?: Maybe<Array<Maybe<Bet>>>;
};


export type Group = {
  __typename?: 'Group';
  id: Scalars['ID'];
  name: Scalars['String'];
  ownerId: Scalars['Int'];
  picture?: Maybe<Scalars['String']>;
  createdAt: Scalars['DateTime'];
  activityAt: Scalars['DateTime'];
  deletedAt?: Maybe<Scalars['DateTime']>;
  owner?: Maybe<User>;
  members?: Maybe<Array<Maybe<User>>>;
  allBets?: Maybe<Array<Maybe<Bet>>>;
  messages?: Maybe<Array<Maybe<GroupChat>>>;
};

export type Bet = {
  __typename?: 'Bet';
  id: Scalars['ID'];
  authorId: Scalars['Int'];
  groupId: Scalars['Int'];
  title: Scalars['String'];
  details: Scalars['String'];
  createdAt: Scalars['DateTime'];
  activityAt: Scalars['DateTime'];
  expiresAt: Scalars['DateTime'];
  deletedAt?: Maybe<Scalars['DateTime']>;
  state: BetState;
  author?: Maybe<User>;
  group?: Maybe<Group>;
  positions?: Maybe<Array<Maybe<Position>>>;
  messages?: Maybe<Array<Maybe<BetChat>>>;
  watchers?: Maybe<Array<Maybe<User>>>;
  expired?: Maybe<Scalars['Boolean']>;
};

/** An enumeration. */
export enum BetState {
  Open = 'OPEN',
  Expired = 'EXPIRED',
  Cancelled = 'CANCELLED',
  Claimed = 'CLAIMED',
  Disputed = 'DISPUTED',
  Paid = 'PAID'
}

export type Position = {
  __typename?: 'Position';
  id: Scalars['ID'];
  betId: Scalars['Int'];
  title: Scalars['String'];
  minimum: Scalars['Int'];
  maximum: Scalars['Int'];
  bet?: Maybe<Bet>;
  userPositions?: Maybe<Array<Maybe<UserPosition>>>;
};

export type UserPosition = {
  __typename?: 'UserPosition';
  id: Scalars['ID'];
  userId?: Maybe<Scalars['Int']>;
  positionId?: Maybe<Scalars['Int']>;
  createdAt: Scalars['DateTime'];
  state: PositionState;
  user?: Maybe<User>;
  position?: Maybe<Position>;
};

/** An enumeration. */
export enum PositionState {
  Taken = 'TAKEN',
  Cancelled = 'CANCELLED',
  Claimed = 'CLAIMED'
}

export type BetChat = {
  __typename?: 'BetChat';
  id: Scalars['ID'];
  betId: Scalars['Int'];
  authorId: Scalars['Int'];
  createdAt: Scalars['DateTime'];
  message: Scalars['String'];
  bet?: Maybe<Bet>;
  author?: Maybe<User>;
};

export type GroupChat = {
  __typename?: 'GroupChat';
  id: Scalars['ID'];
  groupId: Scalars['Int'];
  authorId: Scalars['Int'];
  createdAt: Scalars['DateTime'];
  message: Scalars['String'];
  group?: Maybe<Group>;
  author?: Maybe<User>;
};

export type Mutation = {
  __typename?: 'Mutation';
  createGroup?: Maybe<CreateGroup>;
  createBet?: Maybe<CreateBet>;
  createExamples?: Maybe<CreateExamples>;
  takePosition?: Maybe<TakePosition>;
  cancelPosition?: Maybe<CancelPosition>;
  sayGroupChat?: Maybe<SayGroupChat>;
  sayBetChat?: Maybe<SayBetChat>;
  cancelBet?: Maybe<CancelBet>;
  invite?: Maybe<Invite>;
  remove?: Maybe<Remove>;
};


export type MutationCreateGroupArgs = {
  payload: CreateGroupPayload;
};


export type MutationCreateBetArgs = {
  payload: CreateBetPayload;
};


export type MutationTakePositionArgs = {
  payload: PositionPayload;
};


export type MutationCancelPositionArgs = {
  payload: PositionPayload;
};


export type MutationSayGroupChatArgs = {
  payload: GroupChatPayload;
};


export type MutationSayBetChatArgs = {
  payload: BetChatPayload;
};


export type MutationCancelBetArgs = {
  payload: CancelBetPayload;
};


export type MutationInviteArgs = {
  payload: InvitePayload;
};


export type MutationRemoveArgs = {
  payload: RemovePayload;
};

export type CreateGroup = {
  __typename?: 'CreateGroup';
  group?: Maybe<Group>;
  ok?: Maybe<Scalars['Boolean']>;
};

export type CreateGroupPayload = {
  name: Scalars['String'];
};

export type CreateBet = {
  __typename?: 'CreateBet';
  bet?: Maybe<Bet>;
  ok?: Maybe<Scalars['Boolean']>;
};

export type CreateBetPayload = {
  title: Scalars['String'];
  details: Scalars['String'];
  expiresIn: Scalars['Int'];
  groupId: Scalars['Int'];
  arbitrary?: Maybe<Scalars['Boolean']>;
};

export type CreateExamples = {
  __typename?: 'CreateExamples';
  ok?: Maybe<Scalars['Boolean']>;
};

export type TakePosition = {
  __typename?: 'TakePosition';
  bet?: Maybe<Bet>;
  ok?: Maybe<Scalars['Boolean']>;
};

export type PositionPayload = {
  betId: Scalars['Int'];
  position?: Maybe<Scalars['String']>;
};

export type CancelPosition = {
  __typename?: 'CancelPosition';
  bet?: Maybe<Bet>;
  ok?: Maybe<Scalars['Boolean']>;
};

export type SayGroupChat = {
  __typename?: 'SayGroupChat';
  message?: Maybe<GroupChat>;
  ok?: Maybe<Scalars['Boolean']>;
};

export type GroupChatPayload = {
  groupId: Scalars['Int'];
  message?: Maybe<Scalars['String']>;
};

export type SayBetChat = {
  __typename?: 'SayBetChat';
  message?: Maybe<BetChat>;
  ok?: Maybe<Scalars['Boolean']>;
};

export type BetChatPayload = {
  betId: Scalars['Int'];
  message?: Maybe<Scalars['String']>;
};

export type CancelBet = {
  __typename?: 'CancelBet';
  ok?: Maybe<Scalars['Boolean']>;
};

export type CancelBetPayload = {
  betId: Scalars['Int'];
};

export type Invite = {
  __typename?: 'Invite';
  ok?: Maybe<Scalars['Boolean']>;
};

export type InvitePayload = {
  groupId: Scalars['Int'];
  email: Scalars['String'];
};

export type Remove = {
  __typename?: 'Remove';
  ok?: Maybe<Scalars['Boolean']>;
};

export type RemovePayload = {
  groupId: Scalars['Int'];
  userId: Scalars['Int'];
};

export type LoadGroupQueryVariables = Exact<{
  groupId?: Maybe<Scalars['Int']>;
}>;


export type LoadGroupQuery = (
  { __typename?: 'Query' }
  & { groups?: Maybe<Array<Maybe<(
    { __typename?: 'Group' }
    & GroupFieldsFragment
  )>>> }
);

export type GroupFieldsFragment = (
  { __typename?: 'Group' }
  & Pick<Group, 'id' | 'name'>
);

export type CreateExamplesMutationVariables = Exact<{ [key: string]: never; }>;


export type CreateExamplesMutation = (
  { __typename?: 'Mutation' }
  & { createExamples?: Maybe<(
    { __typename?: 'CreateExamples' }
    & Pick<CreateExamples, 'ok'>
  )> }
);

export type SayGroupChatMutationVariables = Exact<{
  groupId: Scalars['Int'];
  message?: Maybe<Scalars['String']>;
}>;


export type SayGroupChatMutation = (
  { __typename?: 'Mutation' }
  & { sayGroupChat?: Maybe<(
    { __typename?: 'SayGroupChat' }
    & Pick<SayGroupChat, 'ok'>
    & { message?: Maybe<(
      { __typename?: 'GroupChat' }
      & Pick<GroupChat, 'id'>
    )> }
  )> }
);

export const GroupFieldsFragmentDoc = gql`
    fragment GroupFields on Group {
  id
  name
}
    `;
export const LoadGroupDocument = gql`
    query loadGroup($groupId: Int) {
  groups(groupId: $groupId) {
    ...GroupFields
  }
}
    ${GroupFieldsFragmentDoc}`;
export const CreateExamplesDocument = gql`
    mutation createExamples {
  createExamples {
    ok
  }
}
    `;
export const SayGroupChatDocument = gql`
    mutation sayGroupChat($groupId: Int!, $message: String) {
  sayGroupChat(payload: {groupId: $groupId, message: $message}) {
    message {
      id
    }
    ok
  }
}
    `;

export type SdkFunctionWrapper = <T>(action: () => Promise<T>) => Promise<T>;


const defaultWrapper: SdkFunctionWrapper = sdkFunction => sdkFunction();
export function getSdk(client: GraphQLClient, withWrapper: SdkFunctionWrapper = defaultWrapper) {
  return {
    loadGroup(variables?: LoadGroupQueryVariables, requestHeaders?: Headers): Promise<LoadGroupQuery> {
      return withWrapper(() => client.request<LoadGroupQuery>(print(LoadGroupDocument), variables, requestHeaders));
    },
    createExamples(variables?: CreateExamplesMutationVariables, requestHeaders?: Headers): Promise<CreateExamplesMutation> {
      return withWrapper(() => client.request<CreateExamplesMutation>(print(CreateExamplesDocument), variables, requestHeaders));
    },
    sayGroupChat(variables: SayGroupChatMutationVariables, requestHeaders?: Headers): Promise<SayGroupChatMutation> {
      return withWrapper(() => client.request<SayGroupChatMutation>(print(SayGroupChatDocument), variables, requestHeaders));
    }
  };
}
export type Sdk = ReturnType<typeof getSdk>;