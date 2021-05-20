// NV GPU compute capability detection.
// build: nvcc arch-test.cu && ./a.out
//
// Refs: <https://github.com/BVLC/caffe/blob/master/cmake/Cuda.cmake#L18-L31>
#include <cstdio>
int main()
{
  int count = 0;
  if (cudaSuccess != cudaGetDeviceCount(&count)) return -1;
  if (count == 0) return -1;
  for (int device = 0; device < count; ++device)
  {
    cudaDeviceProp prop;
    if (cudaSuccess == cudaGetDeviceProperties(&prop, device))
      std::printf("%d.%d \n", prop.major, prop.minor);
  }
  return 0;
}
