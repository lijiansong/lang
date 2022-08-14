#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct _block_t {
  struct _block_t *next;
  struct _block_t *prev;
  int _offset;
  int _size;
  int _flags; // 0: free, 1: taken
} block_t;

block_t *find_free_block(block_t *head, int req_size) {
  block_t *it = head;
  while (it != NULL) {
    if (it->_size >= req_size && it->_flags == 0) {
      break;
    }
    it = it->next;
  }
  return it;
}

void split_block(block_t *chunk, int req_size) {
  block_t *new_block = (block_t *)malloc(sizeof(block_t));
  new_block->_size = req_size;
  new_block->_offset = chunk->_offset;
  // mark block as taken
  new_block->_flags = 1;
  // split block RIGHT, update offset & size of split chunk
  chunk->_offset += req_size;
  chunk->_size -= req_size;
  // update block links
  chunk->prev->next = new_block;
  new_block->prev = chunk->prev;
  new_block->next = chunk;
  chunk->prev = new_block;
}

void malloc_block(block_t *head, int req_size) {
  block_t *block = find_free_block(head, req_size);
  if (!block) {
    // do nothing
    return;
  }
  split_block(block, req_size);
}

block_t *find_block_from_offset(block_t *head, int offset) {
  block_t *it = head;
  while (it != NULL) {
    if (it->_offset == offset && it->_size > 0) {
      break;
    }
    it = it->next;
  }
  return it;
}

void merge_block(block_t *chunk) {
  int free_flag = chunk->_flags;
  // merge with previous block
  if ((chunk->prev != NULL) && (chunk->prev->_size != -1) &&
      (chunk->prev->_flags == free_flag)) {
    block_t *current_chunk = chunk;
    // update block size
    chunk->prev->_size += chunk->_size;
    chunk->prev->next = chunk->next;
    chunk->next->prev = chunk->prev;
    // for this case: free -> taken -> free
    chunk = chunk->prev;
    free(current_chunk);
  }
  // merge with next block
  if ((chunk->next->next != NULL) && (chunk->next->_flags == free_flag)) {
    // update block size
    block_t *next_chunk = chunk->next;
    chunk->_size += chunk->next->_size;
    chunk->next->next->prev = chunk;
    chunk->next = chunk->next->next;
    free(next_chunk);
  }
}

void free_block(block_t *head, int offset) {
  block_t *block = find_block_from_offset(head, offset);
  // FIXME: block not found is undefined!
  if (!block) {
    // do nothing
    return;
  }
  printf("@@@@ free block flag: %d, offset: %d, size: %d\n", block->_flags,
         block->_offset, block->_size);
  // mark block as free
  block->_flags = 0;
  merge_block(block);
}

int **get_ans(block_t *head, int *returnSize) {
  block_t *it = head;
  int count = 0;
  // get returnSize
  while (it != NULL) {
    if (it->_flags == 0 && it->_size > 0) {
      ++count;
    }
    it = it->next;
  }
  int **ans = (int **)malloc(count * sizeof(int *));
  *returnSize = count;
  // get returnColumnSizes
  it = head;
  int i = 0;
  while (it != NULL) {
    if (it->_flags == 0 && it->_size > 0) {
      int *tmp = (int *)malloc(2 * sizeof(int));
      tmp[0] = it->_offset;
      tmp[1] = it->_size;
      ans[i] = tmp;
      ++i;
    }
    it = it->next;
  }
  return ans;
}

void dump_block(block_t *head) {
  printf("++++ --> begin\n");
  block_t *it = head;
  while (it != NULL) {
    printf("++++ flag: %d, offset: %d, size: %d\n", it->_flags, it->_offset,
           it->_size);
    it = it->next;
  }
  printf("++++ --> end\n");
}

// FIXME: requestsColSize ? returnColumnSizes ?
int **mem_operations(int **requests, int requestsSize, int *returnSize) {
  // init memory pool with 2M
  int poolSize = 2 * 1024 * 1024;
  block_t *dummy_head = (block_t *)malloc(sizeof(block_t));
  block_t *head = (block_t *)malloc(sizeof(block_t));
  block_t *dummy_tail = (block_t *)malloc(sizeof(block_t));
  dummy_head->next = head;
  dummy_head->prev = NULL;
  dummy_head->_offset = -1;
  dummy_head->_size = -1; // mark as dummy
  dummy_head->_flags = 1;
  dummy_tail->next = NULL;
  dummy_tail->prev = head;
  dummy_tail->_offset = -1;
  dummy_tail->_size = -1; // mark as dummy
  dummy_tail->_flags = 1;
  head->next = dummy_tail;
  head->prev = dummy_head;
  head->_offset = 0;
  head->_size = poolSize;
  head->_flags = 0; // mark as free
  dump_block(dummy_head);
  // simulate memory operations
  for (int i = 0; i < requestsSize; ++i) {
    printf("==> %d, %d\n", requests[i][0], requests[i][1]);
    // malloc
    if (requests[i][0] == 0) {
      dump_block(dummy_head);
      malloc_block(head, requests[i][1]);
      head = dummy_head->next;
      dump_block(dummy_head);
    }
    // free
    if (requests[i][0] == 1) {
      dump_block(dummy_head);
      free_block(head, requests[i][1]);
      head = dummy_head->next;
      dump_block(dummy_head);
    }
  }
  // dump_block(dummy_head);
  // get output
  int **ans = get_ans(head, returnSize);
  free(dummy_head);
  free(dummy_tail);
  return ans;
}

/**
 * @brief testcases for 'mem_operations'.
 *
 */
int test1() {
  int cnt = 4;
  int in_req[4][2] = {{0, 10}, {0, 20}, {0, 30}, {1, 10}};
  int expect[2][2] = {{10, 20}, {60, 2097092}};
  int **in_preq = (int **)malloc(cnt * sizeof(int *));
  for (int i = 0; i < cnt; ++i) {
    in_preq[i] = in_req[i];
  }
  int out_size = 0;
  int **ans = mem_operations(in_preq, cnt, &out_size);
  bool pass = true;
  printf("out size: %d\n", out_size);
  for (int i = 0; i < out_size; ++i) {
    printf("%d %d\n", ans[i][0], ans[i][1]);
    if ((ans[i][0] != expect[i][0]) || (ans[i][1] != expect[i][1])) {
      pass = false;
    }
  }
  if (pass) {
    printf(">>> \033[0;32mPASS!\033[0m\n");
  } else {
    printf(">>> \033[0;31mFAIL!\033[0m\n");
  }
  for (int i = 0; i < out_size; ++i) {
    free(ans[i]);
  }
  free(in_preq);
  free(ans);
  if (pass) {
    return 1;
  }
  return 0;
}

int test2() {
  int cnt = 5;
  int in_req[5][2] = {{0, 10}, {0, 20}, {0, 30}, {1, 10}, {1, 0}};
  int expect[2][2] = {{0, 30}, {60, 2097092}};
  int **in_preq = (int **)malloc(cnt * sizeof(int *));
  for (int i = 0; i < cnt; ++i) {
    in_preq[i] = in_req[i];
  }
  int out_size = 0;
  int **ans = mem_operations(in_preq, cnt, &out_size);
  bool pass = true;
  printf("out size: %d\n", out_size);
  for (int i = 0; i < out_size; ++i) {
    printf("%d %d\n", ans[i][0], ans[i][1]);
    if ((ans[i][0] != expect[i][0]) || (ans[i][1] != expect[i][1])) {
      pass = false;
    }
  }
  if (pass) {
    printf(">>> \033[0;32mPASS!\033[0m\n");
  } else {
    printf(">>> \033[0;31mFAIL!\033[0m\n");
  }
  for (int i = 0; i < out_size; ++i) {
    free(ans[i]);
  }
  free(in_preq);
  free(ans);
  if (pass) {
    return 1;
  }
  return 0;
}

int test3() {
  int cnt = 4;
  int in_req[4][2] = {{0, 10}, {1, 0}, {0, 20}, {1, 0}};
  int expect[1][2] = {{0, 2097152}};
  int **in_preq = (int **)malloc(cnt * sizeof(int *));
  for (int i = 0; i < cnt; ++i) {
    in_preq[i] = in_req[i];
  }
  int out_size = 0;
  int **ans = mem_operations(in_preq, cnt, &out_size);
  bool pass = true;
  printf("out size: %d\n", out_size);
  for (int i = 0; i < out_size; ++i) {
    printf("%d %d\n", ans[i][0], ans[i][1]);
    if ((ans[i][0] != expect[i][0]) || (ans[i][1] != expect[i][1])) {
      pass = false;
    }
  }
  if (pass) {
    printf(">>> \033[0;32mPASS!\033[0m\n");
  } else {
    printf(">>> \033[0;31mFAIL!\033[0m\n");
  }
  for (int i = 0; i < out_size; ++i) {
    free(ans[i]);
  }
  free(in_preq);
  free(ans);
  if (pass) {
    return 1;
  }
  return 0;
}

int test4() {
  int cnt = 2;
  int in_req[2][2] = {{0, 10000}, {1, 0}};
  int expect[1][2] = {{0, 2097152}};
  int **in_preq = (int **)malloc(cnt * sizeof(int *));
  for (int i = 0; i < cnt; ++i) {
    in_preq[i] = in_req[i];
  }
  int out_size = 0;
  int **ans = mem_operations(in_preq, cnt, &out_size);
  bool pass = true;
  printf("out size: %d\n", out_size);
  for (int i = 0; i < out_size; ++i) {
    printf("%d %d\n", ans[i][0], ans[i][1]);
    if ((ans[i][0] != expect[i][0]) || (ans[i][1] != expect[i][1])) {
      pass = false;
    }
  }
  if (pass) {
    printf(">>> \033[0;32mPASS!\033[0m\n");
  } else {
    printf(">>> \033[0;31mFAIL!\033[0m\n");
  }
  for (int i = 0; i < out_size; ++i) {
    free(ans[i]);
  }
  free(in_preq);
  free(ans);
  if (pass) {
    return 1;
  }
  return 0;
}

int test5() {
  int cnt = 4;
  int in_req[4][2] = {{0, 1000}, {0, 1000}, {1, 0}, {1, 1000}};
  int expect[1][2] = {{0, 2097152}};
  int **in_preq = (int **)malloc(cnt * sizeof(int *));
  for (int i = 0; i < cnt; ++i) {
    in_preq[i] = in_req[i];
  }
  int out_size = 0;
  int **ans = mem_operations(in_preq, cnt, &out_size);
  bool pass = true;
  printf("out size: %d\n", out_size);
  for (int i = 0; i < out_size; ++i) {
    printf("%d %d\n", ans[i][0], ans[i][1]);
    if ((ans[i][0] != expect[i][0]) || (ans[i][1] != expect[i][1])) {
      pass = false;
    }
  }
  if (pass) {
    printf(">>> \033[0;32mPASS!\033[0m\n");
  } else {
    printf(">>> \033[0;31mFAIL!\033[0m\n");
  }
  for (int i = 0; i < out_size; ++i) {
    free(ans[i]);
  }
  free(in_preq);
  free(ans);
  if (pass) {
    return 1;
  }
  return 0;
}

int test6() {
  int cnt = 6;
  int in_req[6][2] = {{0, 1000}, {0, 1000}, {1, 0},
                      {1, 1000}, {0, 1000}, {0, 1000}};
  int expect[1][2] = {{2000, 2095152}};
  int **in_preq = (int **)malloc(cnt * sizeof(int *));
  for (int i = 0; i < cnt; ++i) {
    in_preq[i] = in_req[i];
  }
  int out_size = 0;
  int **ans = mem_operations(in_preq, cnt, &out_size);
  bool pass = true;
  printf("out size: %d\n", out_size);
  for (int i = 0; i < out_size; ++i) {
    printf("%d %d\n", ans[i][0], ans[i][1]);
    if ((ans[i][0] != expect[i][0]) || (ans[i][1] != expect[i][1])) {
      pass = false;
    }
  }
  if (pass) {
    printf(">>> \033[0;32mPASS!\033[0m\n");
  } else {
    printf(">>> \033[0;31mFAIL!\033[0m\n");
  }
  for (int i = 0; i < out_size; ++i) {
    free(ans[i]);
  }
  free(in_preq);
  free(ans);
  if (pass) {
    return 1;
  }
  return 0;
}

int test7() {
  int cnt = 6;
  int in_req[6][2] = {{0, 1000}, {0, 1000}, {0, 100},
                      {1, 0},    {1, 2000}, {0, 1000}};
  int expect[1][2] = {{2000, 2095152}};
  int **in_preq = (int **)malloc(cnt * sizeof(int *));
  for (int i = 0; i < cnt; ++i) {
    in_preq[i] = in_req[i];
  }
  int out_size = 0;
  int **ans = mem_operations(in_preq, cnt, &out_size);
  bool pass = true;
  printf("out size: %d\n", out_size);
  for (int i = 0; i < out_size; ++i) {
    printf("%d %d\n", ans[i][0], ans[i][1]);
    if ((ans[i][0] != expect[i][0]) || (ans[i][1] != expect[i][1])) {
      pass = false;
    }
  }
  if (pass) {
    printf(">>> \033[0;32mPASS!\033[0m\n");
  } else {
    printf(">>> \033[0;31mFAIL!\033[0m\n");
  }
  for (int i = 0; i < out_size; ++i) {
    free(ans[i]);
  }
  free(in_preq);
  free(ans);
  if (pass) {
    return 1;
  }
  return 0;
}

int test8() {
  int cnt = 1;
  int in_req[1][2] = {{0, 2000}};
  int expect[1][2] = {{2000, 2095152}};
  int **in_preq = (int **)malloc(cnt * sizeof(int *));
  for (int i = 0; i < cnt; ++i) {
    in_preq[i] = in_req[i];
  }
  int out_size = 0;
  int **ans = mem_operations(in_preq, cnt, &out_size);
  bool pass = true;
  printf("out size: %d\n", out_size);
  for (int i = 0; i < out_size; ++i) {
    printf("%d %d\n", ans[i][0], ans[i][1]);
    if ((ans[i][0] != expect[i][0]) || (ans[i][1] != expect[i][1])) {
      pass = false;
    }
  }
  if (pass) {
    printf(">>> \033[0;32mPASS!\033[0m\n");
  } else {
    printf(">>> \033[0;31mFAIL!\033[0m\n");
  }
  for (int i = 0; i < out_size; ++i) {
    free(ans[i]);
  }
  free(in_preq);
  free(ans);
  if (pass) {
    return 1;
  }
  return 0;
}

int test9() {
  int cnt = 1;
  int in_req[1][2] = {{0, 2097153}};
  int expect[1][2] = {{0, 2097152}};
  int **in_preq = (int **)malloc(cnt * sizeof(int *));
  for (int i = 0; i < cnt; ++i) {
    in_preq[i] = in_req[i];
  }
  int out_size = 0;
  int **ans = mem_operations(in_preq, cnt, &out_size);
  bool pass = true;
  printf("out size: %d\n", out_size);
  for (int i = 0; i < out_size; ++i) {
    printf("%d %d\n", ans[i][0], ans[i][1]);
    if ((ans[i][0] != expect[i][0]) || (ans[i][1] != expect[i][1])) {
      pass = false;
    }
  }
  if (pass) {
    printf(">>> \033[0;32mPASS!\033[0m\n");
  } else {
    printf(">>> \033[0;31mFAIL!\033[0m\n");
  }
  for (int i = 0; i < out_size; ++i) {
    free(ans[i]);
  }
  free(in_preq);
  free(ans);
  if (pass) {
    return 1;
  }
  return 0;
}

// FIXME: this behavbior is undefined!!!
int test10() {
  int cnt = 1;
  int in_req[1][2] = {{0, 2097152}};
  int expect[1][2] = {{2097152, 0}};
  int **in_preq = (int **)malloc(cnt * sizeof(int *));
  for (int i = 0; i < cnt; ++i) {
    in_preq[i] = in_req[i];
  }
  int out_size = 0;
  int **ans = mem_operations(in_preq, cnt, &out_size);
  bool pass = true;
  printf("out size: %d\n", out_size);
  for (int i = 0; i < out_size; ++i) {
    printf("%d %d\n", ans[i][0], ans[i][1]);
    if ((ans[i][0] != expect[i][0]) || (ans[i][1] != expect[i][1])) {
      pass = false;
    }
  }
  if (pass) {
    printf(">>> \033[0;32mPASS!\033[0m\n");
  } else {
    printf(">>> \033[0;31mFAIL!\033[0m\n");
  }
  for (int i = 0; i < out_size; ++i) {
    free(ans[i]);
  }
  free(in_preq);
  free(ans);
  if (pass) {
    return 1;
  }
  return 0;
}

int test11() {
  int cnt = 1;
  int in_req[1][2] = {{0, 2097151}};
  int expect[1][2] = {{2097151, 1}};
  int **in_preq = (int **)malloc(cnt * sizeof(int *));
  for (int i = 0; i < cnt; ++i) {
    in_preq[i] = in_req[i];
  }
  int out_size = 0;
  int **ans = mem_operations(in_preq, cnt, &out_size);
  bool pass = true;
  printf("out size: %d\n", out_size);
  for (int i = 0; i < out_size; ++i) {
    printf("%d %d\n", ans[i][0], ans[i][1]);
    if ((ans[i][0] != expect[i][0]) || (ans[i][1] != expect[i][1])) {
      pass = false;
    }
  }
  if (pass) {
    printf(">>> \033[0;32mPASS!\033[0m\n");
  } else {
    printf(">>> \033[0;31mFAIL!\033[0m\n");
  }
  for (int i = 0; i < out_size; ++i) {
    free(ans[i]);
  }
  free(in_preq);
  free(ans);
  if (pass) {
    return 1;
  }
  return 0;
}

int test12() {
  int cnt = 7;
  int in_req[7][2] = {{0, 2097151}, {1, 0}, {0, 2097151}, {1, 0},
                      {0, 2097151}, {1, 0}, {0, 2097151}};
  int expect[1][2] = {{2097151, 1}};
  int **in_preq = (int **)malloc(cnt * sizeof(int *));
  for (int i = 0; i < cnt; ++i) {
    in_preq[i] = in_req[i];
  }
  int out_size = 0;
  int **ans = mem_operations(in_preq, cnt, &out_size);
  bool pass = true;
  printf("out size: %d\n", out_size);
  for (int i = 0; i < out_size; ++i) {
    printf("%d %d\n", ans[i][0], ans[i][1]);
    if ((ans[i][0] != expect[i][0]) || (ans[i][1] != expect[i][1])) {
      pass = false;
    }
  }
  if (pass) {
    printf(">>> \033[0;32mPASS!\033[0m\n");
  } else {
    printf(">>> \033[0;31mFAIL!\033[0m\n");
  }
  for (int i = 0; i < out_size; ++i) {
    free(ans[i]);
  }
  free(in_preq);
  free(ans);
  if (pass) {
    return 1;
  }
  return 0;
}

int test13() {
  int cnt = 9;
  int in_req[9][2] = {{0, 2097151}, {1, 0}, {0, 2097151},
                      {0, 2097151}, {1, 0}, {0, 2097151},
                      {0, 2097151}, {1, 0}, {0, 2097151}};
  int expect[1][2] = {{2097151, 1}};
  int **in_preq = (int **)malloc(cnt * sizeof(int *));
  for (int i = 0; i < cnt; ++i) {
    in_preq[i] = in_req[i];
  }
  int out_size = 0;
  int **ans = mem_operations(in_preq, cnt, &out_size);
  bool pass = true;
  printf("out size: %d\n", out_size);
  for (int i = 0; i < out_size; ++i) {
    printf("%d %d\n", ans[i][0], ans[i][1]);
    if ((ans[i][0] != expect[i][0]) || (ans[i][1] != expect[i][1])) {
      pass = false;
    }
  }
  if (pass) {
    printf(">>> \033[0;32mPASS!\033[0m\n");
  } else {
    printf(">>> \033[0;31mFAIL!\033[0m\n");
  }
  for (int i = 0; i < out_size; ++i) {
    free(ans[i]);
  }
  free(in_preq);
  free(ans);
  if (pass) {
    return 1;
  }
  return 0;
}

int test14() {
  int cnt = 4;
  int in_req[4][2] = {{0, 1000}, {1, 0}, {0, 500}, {0, 500}};
  int expect[1][2] = {{1000, 2096152}};
  int **in_preq = (int **)malloc(cnt * sizeof(int *));
  for (int i = 0; i < cnt; ++i) {
    in_preq[i] = in_req[i];
  }
  int out_size = 0;
  int **ans = mem_operations(in_preq, cnt, &out_size);
  bool pass = true;
  printf("out size: %d\n", out_size);
  for (int i = 0; i < out_size; ++i) {
    printf("%d %d\n", ans[i][0], ans[i][1]);
    if ((ans[i][0] != expect[i][0]) || (ans[i][1] != expect[i][1])) {
      pass = false;
    }
  }
  if (pass) {
    printf(">>> \033[0;32mPASS!\033[0m\n");
  } else {
    printf(">>> \033[0;31mFAIL!\033[0m\n");
  }
  for (int i = 0; i < out_size; ++i) {
    free(ans[i]);
  }
  free(in_preq);
  free(ans);
  if (pass) {
    return 1;
  }
  return 0;
}

int test15() {
  int cnt = 12;
  int in_req[12][2] = {{0, 1000}, {1, 0},    {0, 500}, {0, 500},
                       {0, 500},  {1, 1000}, {0, 500}, {1, 1000},
                       {0, 500},  {1, 1000}, {0, 500}, {1, 1000}};
  int expect[1][2] = {{1000, 2096152}};
  int **in_preq = (int **)malloc(cnt * sizeof(int *));
  for (int i = 0; i < cnt; ++i) {
    in_preq[i] = in_req[i];
  }
  int out_size = 0;
  int **ans = mem_operations(in_preq, cnt, &out_size);
  bool pass = true;
  printf("out size: %d\n", out_size);
  for (int i = 0; i < out_size; ++i) {
    printf("%d %d\n", ans[i][0], ans[i][1]);
    if ((ans[i][0] != expect[i][0]) || (ans[i][1] != expect[i][1])) {
      pass = false;
    }
  }
  if (pass) {
    printf(">>> \033[0;32mPASS!\033[0m\n");
  } else {
    printf(">>> \033[0;31mFAIL!\033[0m\n");
  }
  for (int i = 0; i < out_size; ++i) {
    free(ans[i]);
  }
  free(in_preq);
  free(ans);
  if (pass) {
    return 1;
  }
  return 0;
}

int test16() {
  int cnt = 8;
  int in_req[8][2] = {{0, 5}, {1, 0}, {0, 1}, {0, 1},
                      {0, 1}, {0, 1}, {0, 1}, {0, 995}};
  int expect[1][2] = {{1000, 2096152}};
  int **in_preq = (int **)malloc(cnt * sizeof(int *));
  for (int i = 0; i < cnt; ++i) {
    in_preq[i] = in_req[i];
  }
  int out_size = 0;
  int **ans = mem_operations(in_preq, cnt, &out_size);
  bool pass = true;
  printf("out size: %d\n", out_size);
  for (int i = 0; i < out_size; ++i) {
    printf("%d %d\n", ans[i][0], ans[i][1]);
    if ((ans[i][0] != expect[i][0]) || (ans[i][1] != expect[i][1])) {
      pass = false;
    }
  }
  if (pass) {
    printf(">>> \033[0;32mPASS!\033[0m\n");
  } else {
    printf(">>> \033[0;31mFAIL!\033[0m\n");
  }
  for (int i = 0; i < out_size; ++i) {
    free(ans[i]);
  }
  free(in_preq);
  free(ans);
  if (pass) {
    return 1;
  }
  return 0;
}

int test17() {
  int cnt = 8;
  int in_req[8][2] = {{0, 2097152}, {1, 0}, {0, 1}, {0, 1},
                      {0, 1},       {0, 1}, {0, 1}, {0, 995}};
  int expect[1][2] = {{1000, 2096152}};
  int **in_preq = (int **)malloc(cnt * sizeof(int *));
  for (int i = 0; i < cnt; ++i) {
    in_preq[i] = in_req[i];
  }
  int out_size = 0;
  int **ans = mem_operations(in_preq, cnt, &out_size);
  bool pass = true;
  printf("out size: %d\n", out_size);
  for (int i = 0; i < out_size; ++i) {
    printf("%d %d\n", ans[i][0], ans[i][1]);
    if ((ans[i][0] != expect[i][0]) || (ans[i][1] != expect[i][1])) {
      pass = false;
    }
  }
  if (pass) {
    printf(">>> \033[0;32mPASS!\033[0m\n");
  } else {
    printf(">>> \033[0;31mFAIL!\033[0m\n");
  }
  for (int i = 0; i < out_size; ++i) {
    free(ans[i]);
  }
  free(in_preq);
  free(ans);
  if (pass) {
    return 1;
  }
  return 0;
}

int test18() {
  int cnt = 10;
  int in_req[10][2] = {{0, 2097152}, {1, 0}, {0, 1},   {0, 1},       {0, 1},
                       {0, 1},       {0, 1}, {0, 995}, {0, 2096152}, {1, 1000}};
  int expect[1][2] = {{1000, 2096152}};
  int **in_preq = (int **)malloc(cnt * sizeof(int *));
  for (int i = 0; i < cnt; ++i) {
    in_preq[i] = in_req[i];
  }
  int out_size = 0;
  int **ans = mem_operations(in_preq, cnt, &out_size);
  bool pass = true;
  printf("out size: %d\n", out_size);
  for (int i = 0; i < out_size; ++i) {
    printf("%d %d\n", ans[i][0], ans[i][1]);
    if ((ans[i][0] != expect[i][0]) || (ans[i][1] != expect[i][1])) {
      pass = false;
    }
  }
  if (pass) {
    printf(">>> \033[0;32mPASS!\033[0m\n");
  } else {
    printf(">>> \033[0;31mFAIL!\033[0m\n");
  }
  for (int i = 0; i < out_size; ++i) {
    free(ans[i]);
  }
  free(in_preq);
  free(ans);
  if (pass) {
    return 1;
  }
  return 0;
}

int test19() {
  int cnt = 14;
  int in_req[14][2] = {{0, 2097152}, {1, 0}, {0, 1},   {0, 1},       {0, 1},
                       {0, 1},       {0, 1}, {0, 995}, {0, 2096152}, {0, 1},
                       {0, 1},       {0, 1}, {0, 1},   {1, 1000}};
  int expect[1][2] = {{1000, 2096152}};
  int **in_preq = (int **)malloc(cnt * sizeof(int *));
  for (int i = 0; i < cnt; ++i) {
    in_preq[i] = in_req[i];
  }
  int out_size = 0;
  int **ans = mem_operations(in_preq, cnt, &out_size);
  bool pass = true;
  printf("out size: %d\n", out_size);
  for (int i = 0; i < out_size; ++i) {
    printf("%d %d\n", ans[i][0], ans[i][1]);
    if ((ans[i][0] != expect[i][0]) || (ans[i][1] != expect[i][1])) {
      pass = false;
    }
  }
  if (pass) {
    printf(">>> \033[0;32mPASS!\033[0m\n");
  } else {
    printf(">>> \033[0;31mFAIL!\033[0m\n");
  }
  for (int i = 0; i < out_size; ++i) {
    free(ans[i]);
  }
  free(in_preq);
  free(ans);
  if (pass) {
    return 1;
  }
  return 0;
}

int test20() {
  int cnt = 12;
  int in_req[12][2] = {{0, 1500}, {0, 1500}, {0, 1500}, {1, 0},
                       {0, 500},  {0, 500},  {0, 500},  {1, 1500},
                       {1, 500},  {1, 1000}, {1, 3000}, {1, 0}};
  int expect[1][2] = {{0, 2097152}};
  int **in_preq = (int **)malloc(cnt * sizeof(int *));
  for (int i = 0; i < cnt; ++i) {
    in_preq[i] = in_req[i];
  }
  int out_size = 0;
  int **ans = mem_operations(in_preq, cnt, &out_size);
  bool pass = true;
  printf("out size: %d\n", out_size);
  for (int i = 0; i < out_size; ++i) {
    printf("%d %d\n", ans[i][0], ans[i][1]);
    if ((ans[i][0] != expect[i][0]) || (ans[i][1] != expect[i][1])) {
      pass = false;
    }
  }
  if (pass) {
    printf(">>> \033[0;32mPASS!\033[0m\n");
  } else {
    printf(">>> \033[0;31mFAIL!\033[0m\n");
  }
  for (int i = 0; i < out_size; ++i) {
    free(ans[i]);
  }
  free(in_preq);
  free(ans);
  if (pass) {
    return 1;
  }
  return 0;
}

void bench() {
  int cnt = 0;
  cnt += test1();
  cnt += test2();
  cnt += test3();
  cnt += test4();
  cnt += test5();
  cnt += test6();
  cnt += test7();
  cnt += test8();
  cnt += test9();
  cnt += test10();
  cnt += test11();
  cnt += test12();
  cnt += test13();
  cnt += test14();
  cnt += test15();
  cnt += test16();
  cnt += test17();
  cnt += test18();
  cnt += test19();
  cnt += test20();
  printf("total pass %d testcases!", cnt);
}

int main() {
  bench();
  return 0;
}
