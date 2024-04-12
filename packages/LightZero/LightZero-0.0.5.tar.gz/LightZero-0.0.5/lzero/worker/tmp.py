if collected_episode >= n_episode:
    # [data, meta_data]
    return_data = [self.game_segment_pool[i][0] for i in range(len(self.game_segment_pool))], [
        {
            'priorities': self.game_segment_pool[i][1],
            'done': self.game_segment_pool[i][2],
            'unroll_plus_td_steps': self.unroll_plus_td_steps
        } for i in range(len(self.game_segment_pool))
    ]
    np.save('/Users/puyuan/code/LightZero/lzero/mcts/tests/pong_muzero_2episodes_gsl400_v0.0.4.npy',
            return_data)
    print('return_data is saved')
    self.game_segment_pool.clear()
    # for i in range(len(self.game_segment_pool)):
    #     print(self.game_segment_pool[i][0].obs_segment.__len__())
    #     print(self.game_segment_pool[i][0].reward_segment)
    # for i in range(len(return_data[0])):
    #     print(return_data[0][i].reward_segment)
    break