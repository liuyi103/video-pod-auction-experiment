#include <cmath>
#include <vector>
#include <map>
#include <algorithm>
#include <assert.h>
#include <cstdlib>
using namespace std;

double random() {
  return rand() * 1.0 / RAND_MAX;
}

class Ad {
public:
  const int duration_;
  const double bid_;
  double price_;
  bool is_fake_;

  Ad(int duration, double bid, bool is_fake) :
   duration_(duration), bid_(bid), is_fake_(is_fake) {
    price_ = bid;
  }
};

void data_sampler(const int n_ad, vector<Ad>* res) {
  assert(res != nullptr);
  res->clear();
  for (int i = 0; i < n_ad; i ++) {
    int duration  = random() * 20 + 10;
    double bid = duration * (1 + random());
    Ad tmp(duration, bid);
    res->push_back(tmp);
  }
}

void select_winners(const vector<Ad>& ads,
                    const int max_duration,
                    vector<Ad>* winners,
                    vector<Ad>* losers) {
  // TODO(lyc): run knapsack with cplex, the winners should contain fake winner.
}

void get_loser_contour(const vector<Ad>& ads,
                       const int max_duration,
                       vector<double>* res) {
  vector<double> dp(max_duration + 1, 0);
  for (Ad ad : ads) {
    for (int i = max_duration; i >= ad.duration_; i --) {
      dp[i] = std::max(dp[i - ad.duration_] + ad.bid_, dp[i]);
    }
  }
  (*res) = dp;
}

void get_winner_contour(vector<Ad>& winners,
                        const int max_duration,
                        vector<double>* contour,
                        vector<vector<bool>>* subsets) {
  vector<double> dp(max_duration + 1, 0);
  vector<vector<bool>>                         
}

int main() {
  vector<Ad> ads;
  data_sampler(10, &ads);
  return 0;
}
