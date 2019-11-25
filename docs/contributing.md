# How to Contribute

## Golden Rules
1. Be kind.
2. Imperfect feedback is [infinitely better](https://en.wikipedia.org/wiki/Perfect_is_the_enemy_of_good) than no feedback at all.

## So you've found a bug or have a suggestion and... 

### You're short on time:
No worries. This will take less than a minute. 
- Go to the github [issues page](https://github.com/jonathanchukinas/fuzzytable/issues/new/choose).
- Select the **Get Started** button next to **Bug report** or **Feature request**
- Fill in the title line.
- Delete the template out the body and briefly describe your issue/feature.
- **Submit new issue**.

### You have a bit more time:
Much appreciated!
- Go to the [github issues page](https://github.com/jonathanchukinas/fuzzytable/issues).
- Click the green **New issue** button.
- Select the **Get Started** button next to **Bug report** or **Feature request**
- Fill in the title line.
- Complete as much of the template prompt questions as you're able.
- **Submit new issue**.

### You'd like to code the solution yourself:

Awesome!!! But first...

#### Ask questions first, shoot later 

If you could, please submit an issue as detailed above.
This allows us to have a conversation about it first and figure out the best solution.
I'd hate for you to do all the work and submit a pull request only to find out it's not a direction we want the project going in.

You can also email fuzzytable.dev@gmail.com, but we'll ultimately end up creating a github issue in order to keep a paper trail. 

#### Developer Steps

1. Fork the fuzzytable repo.

2. Clone and create feature branch 

   ```shell
   $ git clone https://github.com/yourusername/fuzzytable.git
   $ git checkout -b featurename
   ```
   
3. Set up development environment 

   ```shell
   python -m venv .venv
   .venv/scripts/activate   
   pip install flit
   flit install --deps develop --symlink
   ```
   
   If running Windows, replace the ``--symlink`` option with ``--pth-file``. See [flit docs](https://flit.readthedocs.io/en/latest/cmdline.html#flit-install) for explanation.
   
   ```shell
   flit install --deps develop --pth-file
   ```
   
3. Write code.

4. Test
   Write tests in ``/tests``. 
   Use pytest to run tests quickly
    
   ```shell
   pytest
   ```
   
   Run tests and check coverage:
   
   ```shell
   pytest --cov-report term-missing --cov=fuzzytable tests/
   ```
   
   When all tests pass and code has 100% coverage, run tox to ensure the code works in all three python environments:
   
   ```shell
   tox
   ```
   
5. Commit and push to remote

   ```shell
   git commit -am 'featurename'
   git push --set-upstream origin featurename
   ```

6. Create a Pull Request

## Thanks!

❤❤❤

Jonathan
